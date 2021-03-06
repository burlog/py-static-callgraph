# -*- coding: utf-8 -*-
#
# LICENCE       MIT
#
# DESCRIPTION   Callgraph in function defs ast nodes.
#
# AUTHOR        Michal Bukovsky <michal.bukovsky@trilogic.cz>
#

import ast
from types import FunctionType

from callgraph.ast_tree import Node
from callgraph.ast_tree.helpers import VariablesScope

class FunctionDefNode(Node):
    def __init__(self, parent, expr_tree):
        super().__init__(parent, expr_tree)
        self.name = expr_tree.name
        # TODO(burlog): filename, calls from defaults, ...

    def eval_node(self, printer, ctx):
        printer("- Skipping function definition:", self.name)
        while False: yield None

class ClassDefNode(Node):
    def __init__(self, parent, expr_tree):
        super().__init__(parent, expr_tree)
        self.name = expr_tree.name
        self.bases = self.make_nodes(expr_tree.bases)
        self.keywords = self.make_nodes(expr_tree.keywords)
        self.starargs = self.make_node(expr_tree.starargs)
        self.kwargs = self.make_node(expr_tree.kwargs)
        self.body = self.make_nodes(expr_tree.body)
        self.decors = self.make_nodes(expr_tree.decorator_list)

    def eval_node(self, printer, ctx):
        with VariablesScope(ctx) as scope:
            for expr in self.body:
                yield from expr.evaluate(printer, ctx)

