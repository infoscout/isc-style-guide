import unittest

from pylint.testutils import CheckerTestCase as PylintCheckerTestCase, Message, _tokenize_str


class CheckerTestCase(PylintCheckerTestCase, unittest.TestCase):

    def setUp(self):
        self.setup_method()


class TokenCheckerTestCase(CheckerTestCase):

    def assertCodeAddsMessages(self, code, messages=None):
        tokens = _tokenize_str(code)
        context_manager = self.assertNoMessages()

        # Create assertAddsMessages context manager if there are messages
        if messages:
            if isinstance(messages, Message):  # Handle single message
                messages = [messages]
            context_manager = self.assertAddsMessages(*messages)

        # Verify that the provided messages are produced, if any, and not if none
        with context_manager:
            self.checker.process_tokens(tokens)
