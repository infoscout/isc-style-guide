import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DjangoRedundantAllMethodChecker(BaseChecker):
    """
    Checks that Django managers and querysets do not use the all() method redundantly.
    """

    __implements__ = IAstroidChecker

    name = 'django_redundant_all'
    msgs = {
        'C2101': (
            'all() method call is redundant here.',
            'django-all-redundant',
            'Using the all() manager/queryset method is redundant, unless no other manager/queryset methods are used.',
        ),
    }

    def visit_call(self, node):
        # Ignore function calls that are not method calls named 'all'
        if not isinstance(node.func, astroid.Attribute) or node.func.attrname != 'all':
            return

        # If we are chaining methods to the all() queryset method, then the call to all() is redundant,
        # except for all() and delete() methods
        # Two all()s are actually redundant, but we'll get the second one when visiting children
        # so that we don't report them twice
        grandparent = node.parent.parent
        if isinstance(grandparent, astroid.Call) and grandparent.func.attrname not in ('all', 'delete',):
            self.add_message('django-all-redundant', node=node)
            return

        # If we are chaining the all() method to other queryset methods, then the call to all() is also redundant
        for child in node.get_children():
            for grandchild in child.get_children():
                if isinstance(grandchild, astroid.Call):
                    self.add_message('django-all-redundant', node=node)
                    return


def register(linter):
    linter.register_checker(DjangoRedundantAllMethodChecker(linter))
