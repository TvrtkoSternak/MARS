from unittest import TestCase
from unittest import main
import ast
import mars.pattern
import astunparse

from mars.astutils import AstWrapper
from mars.pattern import Insert, Update, Delete, Move


class TestEditScript(TestCase):
    def __init__(self):
        self.wrapper = AstWrapper()

    def test_walk(self):
        source = 'if attr == attr(): \n\tdosomething()'
        body = self.wrapper.visit(ast.parse(source))
        tree = body.walk()
