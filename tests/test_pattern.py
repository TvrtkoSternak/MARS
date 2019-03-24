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
        self.upsert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_simple.py', 2, True)

    def test_ast_insert_middle_of_if_statement(self):
        self.upsert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_middle_of_if.py', 12, True)

    def test_ast_insert_end_of_if_statement(self):
        self.upsert_test('insert/original.py', 'insert/change_simple.py', 'insert/modified_end_of_if.py', 17, True)

    def test_ast_update(self):
        self.upsert_test('test_update_original.py', 'test_update_change.py', 'test_update_modified.py', 12, False)

    def test_ast_delete(self):
        self.delmov_test('test_delete_original.py', 'test_delete_modified.py', 12)

    def upsert_test(self, original_code, change_code, modified_code, index, is_insert):
        with open('resources/'+original_code) as original, \
                open('resources/'+change_code) as change, \
                open('resources/'+modified_code) as modified:
            original_ast = ast.parse(original.read())
            change_ast = ast.parse(change.read())
            modified_ast = ast.parse(modified.read())
            operation = Insert(index, change_ast) if is_insert else Update(index, change_ast)
            operation.make_change(original_ast)
            message = 'Insert test failed, modified codes do not match!' if is_insert \
                else 'Update test failed, modified codes do not match'
            self.assertEqual(astunparse.unparse(original_ast.body),
                             astunparse.unparse(modified_ast.body),
                             msg=message)

    def delmov_test(self, original_code, modified_code, del_index, ins_index=None):
        with open('resources/'+original_code) as original, \
                open('resources/'+modified_code) as modified:
            original_ast = ast.parse(original.read())
            modified_ast = ast.parse(modified.read())
            operation = Delete(del_index) if ins_index is None else Move(ins_index, del_index)
            operation.make_change(original_ast)
            message = 'Delete test failed, modified codes do not match!' if ins_index is None \
                else 'Move test failed, modified codes do not match'
            print(astunparse.unparse(original_ast.body))
            self.assertEqual(astunparse.unparse(original_ast.body),
                             astunparse.unparse(modified_ast.body),
                             msg=message)


if __name__ == 'main':
    main()
