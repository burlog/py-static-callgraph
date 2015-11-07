# -*- coding: utf-8 -*-
#
# LICENCE       MIT
#
# DESCRIPTION   Test suite for free functions.
#
# AUTHOR        Michal Bukovsky <michal.bukovsky@trilogic.cz>
#

import pytest, re
from functools import wraps

from callgraph.builder import CallGraphBuilder
from tests.helpers import dfs_node_names

def test_functions_body():
    def fun1():
        False

    def fun2():
        fun1()

    def fun3():
        fun2()
        fun1()

    builder = CallGraphBuilder()
    root = builder.build(fun3)
    from callgraph.indent_printer import dump_tree
    dump_tree(root, lambda x: x.children)

    path = ["fun3", "fun3.fun2", "fun3.fun2.fun1", "fun3.fun1"]
    assert list(dfs_node_names(root)) == path

def test_functions_recur():
    def recur():
        recur()

    builder = CallGraphBuilder()
    root = builder.build(recur)

    path = ["recur"]
    assert list(dfs_node_names(root)) == path

def test_functions_nested():
    def nester():
        def nested():
            pass
        def invisible():
            nested()
        nested()

    builder = CallGraphBuilder()
    root = builder.build(nester)
    from callgraph.indent_printer import dump_tree
    dump_tree(root, lambda x: x.children)

    path = ["nester", "nester.nested"]
    assert list(dfs_node_names(root)) == path

def test_functions_stored_fun():
    def fun1():
        "".strip()

    def fun():
        a = fun1
        a()

    builder = CallGraphBuilder()
    root = builder.build(fun)
    from callgraph.indent_printer import dump_tree
    dump_tree(root, lambda x: x.children)

    path = ["fun", "fun.fun1", "fun.fun1.strip"]
    assert list(dfs_node_names(root)) == path

def test_functions_return_chain():
    def fun2():
        return ""

    def fun1():
        return fun2()

    def fun():
        a = fun1()
        a.strip()

    builder = CallGraphBuilder()
    root = builder.build(fun)
    from callgraph.indent_printer import dump_tree
    dump_tree(root, lambda x: x.children)

    path = ["fun", "fun.fun1", "fun.fun1.fun2", "fun.strip"]
    assert list(dfs_node_names(root)) == path

#def test_default_arg():
#    def func_def(x=None, e=error_1):
#        if x: raise e
#    res = zip(*gather_symbols(func_def, matcher_re.match))[0]
#    assert res == ("error_1", )
#
#@pytest.mark.skipif(True, reason="TODO")
#def test_default_arg_func():
#    def arg():
#        return error_1
#    def func_def(x=None, e=arg()):
#        if x: raise e
#    res = zip(*gather_symbols(func_def, matcher_re.match))[0]
#    assert res == ("error_1", )
#
#@pytest.mark.skipif(True, reason="TODO")
#def test_gener():
#    def gener():
#        yield error_1
#    res = zip(*gather_symbols(gener, matcher_re.match))[0]
#    assert res == ("error_1", )
#
#    def for_with_gener():
#        for a in  gener():
#            raise error_2
#    res = zip(*gather_symbols(for_with_gener, matcher_re.match))[0]
#    assert res == ("error_1", "error_2")

