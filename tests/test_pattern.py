from unittest import TestCase
from unittest import main
import ast
import mars.pattern
import astunparse
from mars.pattern import Insert, Update, Delete, Move


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

    def test_ast_insert_simple(self):
        self.insert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_simple.py', 5)

    def test_ast_insert_start_of_if_statement(self):
        self.insert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_start_of_if.py', 11)

    def test_ast_insert_middle_of_if_statement(self):
        self.insert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_middle_of_if.py', 16)

    def test_ast_insert_end_of_if_statement(self):
        self.insert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_end_of_if.py', 33)

    def test_ast_update(self):
        self.update_test('test_update_original.py', 'test_update_change.py', 'test_update_modified.py', 11)

    def test_ast_delete(self):
        self.delete_test('test_delete_original.py', 'test_delete_modified.py', 11)

    def test_ast_delete_simple(self):
        self.delete_test('delete/original.py', 'delete/modified.py', 11)

    def test_ast_move(self):
        self.move_test('move/original.py', 'move/modified.py', 33, 11)

    #region HELPERS
    def insert_test(self, original_code, change_code, modified_code, index):
        self.run_test(original_code, modified_code, index, 'insert', change_code)

    def update_test(self, original_code, change_code, modified_code, index):
        self.run_test(original_code, modified_code, index, 'update', change_code)

    def delete_test(self, original_code, modified_code, index):
        self.run_test(original_code, modified_code, index, 'delete')

    def move_test(self, original_code, modified_code, delete_index, insert_index):
        self.run_test(original_code, modified_code, delete_index, 'move', second_index=insert_index)

    def run_test(self, original_code, modified_code, index, operation_name, change_code=None, second_index=0):
        change_ast = None
        with open('resources/' + original_code) as original, open('resources/' + modified_code) as modified:
            original_ast = ast.parse(original.read())
            modified_ast = ast.parse(modified.read())
        if change_code is not None:
            with open('resources/'+change_code) as change:
                change_ast = ast.parse(change.read())

        operation = {
            'insert': Insert(index, change_ast),
            'update': Update(index, change_ast),
            'delete': Delete(index),
            'move': Move(second_index, index)
        }[operation_name]

        operation.make_change(original_ast)

        self.assertEqual(astunparse.unparse(original_ast.body), astunparse.unparse(modified_ast.body))
    #endregion


if __name__ == 'main':
    main()
