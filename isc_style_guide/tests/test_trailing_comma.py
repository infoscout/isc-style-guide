from pylint.testutils import Message

from isc_style_guide.checkers.trailing_comma import IterableTrailingCommaChecker
from isc_style_guide.tests.utils import TokenCheckerTestCase


class TestIterableTrailingCommaChecker(TokenCheckerTestCase):

    CHECKER_CLASS = IterableTrailingCommaChecker

    def testInlineTupleTrailingComma(self):
        # Verify that a tuple that does not end in a trailing comma does produce a message
        self.assertCodeAddsMessages("x = (1, 2)", Message('tuple-missing-trailing-comma', line=1))

        # Verify that a tuple ending with a trailing comma does not produce any messages
        self.assertCodeAddsMessages("x = (1, 2,)")

    def testFunctionSignatureIsNotConsideredTuple(self):
        code = """
            def foo(x, y):
                pass
        """
        self.assertCodeAddsMessages(code)

    def testMethodCallIsNotConsideredTuple(self):
        code = """
            self.foo(x, y)
        """
        self.assertCodeAddsMessages(code)

    def testMethodCallUsingGetattrIsNotConsideredTuple(self):
        code = """
            getattr(self, 'foo')(x, y)
        """
        self.assertCodeAddsMessages(code)

    def testMultilineIterableTrailingComma(self):
        # Verify that a multiline iterable that does not end in a trailing comma does produce a message
        code = """
            x = (
                1,
                2
            )
            y = [
                1,
                2
            ]
            z = {
                1,
                2
            }
            d = {
                'a': 1,
                'b': 2
            }
        """
        messages = [
            Message('tuple-missing-trailing-comma', line=4),
            Message('multiline-iterable-missing-trailing-comma', line=8),
            Message('multiline-iterable-missing-trailing-comma', line=12),
            Message('multiline-iterable-missing-trailing-comma', line=16),
        ]
        self.assertCodeAddsMessages(code, messages)

        # Verify that a multiline iterable ending in a trailing comma does not produce any messages
        code = """
            x = (
                1,
                2,
            )
            y = [
                1,
                2,
            ]
            z = {
                1,
                2,
            }
            d = {
                'a': 1,
                'b': 2,
            }
        """
        self.assertCodeAddsMessages(code)

    def testMultilineIterableImmediatelyAfterFunctionCallTrailingComma(self):
        code = """
            bar = foo()
            (
                x, y, z
            ) = bar
        """
        self.assertCodeAddsMessages(code, Message('tuple-missing-trailing-comma', line=4))

    def testMultilineIterableSingleItemTrailingComma(self):
        # Verify that a multiline iterable (even with just a single item) produces a message
        # if it does end in a trailing comma
        code = """
            x = [
                1
            ]
            y = {
                1
            }
            z = {
                'a': 1
            }
        """
        messages = [
            Message('multiline-iterable-missing-trailing-comma', line=3),
            Message('multiline-iterable-missing-trailing-comma', line=6),
            Message('multiline-iterable-missing-trailing-comma', line=9),
        ]
        self.assertCodeAddsMessages(code, messages)

    def testMultilineIterableTrailingCommaIgnoresComments(self):
        # Verify that a multiline iterable ending in a trailing comma (with comments) does not produce any messages
        code = """
            x = (
                1,
                2,  # comment
            )
            y = [
                1,
                2,  # comment
            ]
            z = {
                1,
                2,  # comment
            }
            d = {
                'a': 1,
                'b': 2,  # comment
            }
        """
        self.assertCodeAddsMessages(code)

    def testDictionaryAccessIsNotConsideredList(self):
        code = """
            d[
                1
            ]
        """
        self.assertCodeAddsMessages(code)

    def testComprehensionsDoNotRequireTrailingComma(self):
        code = """
            x = (
                i for i in range(10)
            )
            y = [
                i for i in range(10)
            ]
            z = {
                i for i in range(10)
            }
            d = {
                i: i for i in range(10)
            }
        """
        self.assertCodeAddsMessages(code)

    def testInlineIterableNoTrailingComma(self):
        # Verify that an inline list, set, or dict that ends in a trailing comma produces a message
        code = """
            x = [1, 2,]
            y = {1, 2,}
            z = {'a': 1, 'b': 2,}
        """
        messages = [
            Message('inline-iterable-trailing-comma', line=2),
            Message('inline-iterable-trailing-comma', line=3),
            Message('inline-iterable-trailing-comma', line=4),
        ]
        self.assertCodeAddsMessages(code, messages)

        # Verify that an inline list, set, and dict without trailing commas does not produce any messages
        code = """
            x = [1, 2]
            y = {1, 2}
            z = {'a': 1, 'b': 2}
        """
        self.assertCodeAddsMessages(code)
