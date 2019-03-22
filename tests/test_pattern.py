from unittest import TestCase
from unittest import main
import ast
import mars.pattern
import astunparse
from mars.pattern import Insert
from mars.pattern import Update


class TestEditScript(TestCase):
    def test_iterating_edit_script(self):
        """
        Test that checks iterating through change operations.
        """
        insert = mars.pattern.Insert(1, ast.Add)
        changes = [insert]
        edit_script = mars.pattern.EditScript(changes)
        it = iter(edit_script)
        self.assertEqual(next(it), insert)
        with self.assertRaises(StopIteration):
            next(it)
        i = 0
        for _ in edit_script:
            i = i + 1
        self.assertEqual(i, 1)

    def test_ast_insert(self):
        with open('resources/test_insert_original.py') as original, \
                open('resources/test_insert_change.py') as change, \
                open('resources/test_insert_modified.py') as modified:
            original_ast = ast.parse(original.read())
            change_ast = ast.parse(change.read())
            modified_ast = ast.parse(modified.read())
            insert = Insert(24, change_ast)
            insert.make_change(original_ast)
            self.assertEqual(astunparse.unparse(original_ast.body),
                             astunparse.unparse(modified_ast.body))

    def test_ast_update(self):
        with open('resources/test_update_original.py') as original, \
                open('resources/test_update_change.py') as change, \
                open('resources/test_update_modified.py') as modified:
            original_ast = ast.parse(original.read())
            change_ast = ast.parse(change.read())
            modified_ast = ast.parse(modified.read())
            update = Update(12, change_ast)
            update.make_change(original_ast)
            self.assertEqual(astunparse.unparse(original_ast.body),
                             astunparse.unparse(modified_ast.body))


if __name__ == 'main':
    main()
