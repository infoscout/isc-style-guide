from collections import namedtuple
import tokenize

from pylint.checkers import BaseTokenChecker
from pylint.interfaces import ITokenChecker


PotentialIterable = namedtuple('PotentialIterable', ['bracket_type', 'status', 'start_row'])


class IterableTrailingCommaChecker(BaseTokenChecker):
    """
    Checks that inline tuples and multiline iterables end with trailing commas,
    whereas other inline iterables do not end in trailing commas.
    """

    BRACKET_TYPE_PAREN = 0
    BRACKET_TYPE_SQUARE = 1
    BRACKET_TYPE_BRACE = 2
    TOKEN_TO_BRACKET_TYPE = {
        '(': BRACKET_TYPE_PAREN,
        '[': BRACKET_TYPE_SQUARE,
        '{': BRACKET_TYPE_BRACE,
    }

    # The brackets definitely does not represent an iterable (eg. function call, dictionary access)
    ITERABLE_STATUS_NO = 0
    # The brackets may represent an iterable, but it also might not be (eg. ambiguous single item tuple)
    ITERABLE_STATUS_POSSIBLE = 1
    ITERABLE_STATUS_DEFINITELY = 2  # The brackets definitely represent an iterable (eg. multi item tuple, braces)

    __implements__ = ITokenChecker

    name = 'iterable_trailing_commas'
    msgs = {
        'C2001': (
            'Missing trailing comma at the end of a tuple.',
            'tuple-missing-trailing-comma',
            'Tuples should always end in a trailing comma.',
        ),
        'C2002': (
            'Missing trailing comma at the end of a multiline iterable.',
            'multiline-iterable-missing-trailing-comma',
            'Multiline iterables should always end in a trailing comma.',
        ),
        'C2003': (
            'Inline iterable ends in trailing comma.',
            'inline-iterable-trailing-comma',
            'Inline iterables should not end in a trailing comma, except for tuples.',
        ),
    }

    def process_tokens(self, tokens):
        last_token_type = last_token = last_token_erow = None
        current_iterables = []

        for token_type, token, (srow, _,), (erow, _,), _ in tokens:
            # Ignore comments and whitespace tokens
            if token_type == tokenize.COMMENT or token == '\n':
                continue

            # Assume for now that the next potential iterable will definitely be one
            iterable_status = self.ITERABLE_STATUS_DEFINITELY

            # If we see an open paren, downgrade the status to possible
            # unless we can immediately determine that this is definitely not a tuple
            if token == '(':
                if last_token_type == tokenize.NAME:
                    iterable_status = self.ITERABLE_STATUS_NO
                else:
                    iterable_status = self.ITERABLE_STATUS_POSSIBLE

            # If we see an open square bracket, determine if this may represent something that's definitely not a list
            elif token == '[':
                if last_token_type == tokenize.NAME:
                    iterable_status = self.ITERABLE_STATUS_NO
                else:
                    iterable_status = self.ITERABLE_STATUS_DEFINITELY

            # Create a new potential iterable when we see an open bracket
            if token in ('(', '[', '{',):
                new_iterable = PotentialIterable(
                    bracket_type=self.TOKEN_TO_BRACKET_TYPE[token],
                    status=iterable_status,
                    start_row=srow
                )
                current_iterables.append(new_iterable)

            # Add any appropriate messages when we reach the end of an iterable
            elif token in (')', ']', '}',):
                finished_iterable = current_iterables.pop()
                if finished_iterable.status == self.ITERABLE_STATUS_DEFINITELY:
                    # Tuples should end in a trailing comma
                    if finished_iterable.bracket_type == self.BRACKET_TYPE_PAREN and last_token != ',':
                        self.add_message('tuple-missing-trailing-comma', line=last_token_erow)
                    # Multiline iterables should end in a trailing comma
                    elif finished_iterable.start_row != erow and last_token != ',':
                        self.add_message('multiline-iterable-missing-trailing-comma', line=last_token_erow)
                    # Inline iterables should not end in a trailing comma (except for tuples)
                    elif (
                        finished_iterable.bracket_type != self.BRACKET_TYPE_PAREN
                        and finished_iterable.start_row == erow
                        and last_token == ','
                    ):
                        self.add_message('inline-iterable-trailing-comma', line=erow)

            # If we see a comma while in a single-item tuple, we can promote it to definitely a tuple
            if token == ',' and current_iterables and current_iterables[-1].bracket_type == self.BRACKET_TYPE_PAREN:
                current_iterable = current_iterables.pop()
                if current_iterable.status == self.ITERABLE_STATUS_POSSIBLE:
                    current_iterable = PotentialIterable(
                        bracket_type=self.BRACKET_TYPE_PAREN,
                        status=self.ITERABLE_STATUS_DEFINITELY,
                        start_row=current_iterable.start_row
                    )
                current_iterables.append(current_iterable)

            # Record information about the last token
            last_token_type = token_type
            last_token = token
            last_token_erow = erow


def register(linter):
    linter.register_checker(IterableTrailingCommaChecker(linter))
