import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DjangoRedundantAllMethodChecker(BaseChecker):
    """
    Checks that Django managers and querysets do not use the all() method redundantly.
    """

    # Includes all built-in queryset methods, excluding all() and delete()
    DJANGO_QUERYSET_REDUNDANT_METHODS = set([
        'filter', 'exclude', 'annotate', 'order_by', 'reverse', 'distinct', 'values', 'values_list', 'dates',
        'datetimes', 'none', 'union', 'intersection', 'difference', 'select_related', 'prefetch_related', 'extra',
        'defer', 'only', 'using', 'select_for_update', 'raw', 'get', 'create', 'get_or_create', 'update_or_create',
        'bulk_create', 'count', 'in_bulk', 'iterator', 'latest', 'earliest', 'first', 'last', 'aggregate', 'exists',
        'update', 'as_manager',
    ])

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
        if (
            isinstance(grandparent, astroid.Call)
            and grandparent.func.attrname in self.DJANGO_QUERYSET_REDUNDANT_METHODS
        ):
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
