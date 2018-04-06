import astroid
from pylint.testutils import Message

from isc_style_guide.checkers.django_redundant_all import DjangoRedundantAllMethodChecker
from isc_style_guide.tests.utils import CheckerTestCase


class TestDjangoRedundantAllMethodChecker(CheckerTestCase):

    CHECKER_CLASS = DjangoRedundantAllMethodChecker

    def testMethodsBeforeAllAreRedundant(self):
        # No messages while visiting the filter node
        filter_node = astroid.extract_node("__(User.objects.filter(is_staff=True)).all()")
        with self.assertNoMessages():
            self.checker.visit_call(filter_node)

        # When we visit the all node, we realize that it is redundant
        all_node = astroid.extract_node("__(User.objects.filter(is_staff=True).all())")
        with self.assertAddsMessages(Message('django-all-redundant', node=all_node)):
            self.checker.visit_call(all_node)

    def testMethodsAfterAllAreRedundant(self):
        # When we visit the all node, we realize that it is going to be redundant
        # with the following filter()
        all_node = astroid.extract_node("__(User.objects.all()).filter(is_staff=True)")
        with self.assertAddsMessages(Message('django-all-redundant', node=all_node)):
            self.checker.visit_call(all_node)

        # No messages while visiting the filter node
        filter_node = astroid.extract_node("__(User.objects.all().filter(is_staff=True))")
        with self.assertNoMessages():
            self.checker.visit_call(filter_node)

    def testAllBeforeDeleteIsNotRedundant(self):
        all_node = astroid.extract_node("__(User.objects.all()).delete()")
        delete_node = astroid.extract_node("__(User.objects.all().delete())")
        with self.assertNoMessages():
            for node in (all_node, delete_node,):
                self.checker.visit_call(node)

    def testTwoAllsAreRedundant(self):
        # We don't have a problem when we visit the first all()
        first_all_node = astroid.extract_node("__(User.objects.all()).all()")
        with self.assertNoMessages():
            self.checker.visit_call(first_all_node)

        # But when we visit the second all(), we realize that is redundant
        second_all_node = astroid.extract_node("__(User.objects.all().all())")
        with self.assertAddsMessages(Message('django-all-redundant', node=second_all_node)):
            self.checker.visit_call(second_all_node)

    def testCustomMethodsCannotBeConsideredRedundant(self):
        all_node = astroid.extract_node("__(User.objects.all()).custom_method()")
        custom_method_node = astroid.extract_node("__(User.objects.all().custom_method())")
        with self.assertNoMessages():
            for node in (all_node, custom_method_node,):
                self.checker.visit_call(node)
