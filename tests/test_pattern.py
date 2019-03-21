from unittest import TestCase
from unittest import main
import ast
import mars.pattern


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
        for e in edit_script:
            i = i + 1
        self.assertEqual(i, 1)

    def test_ast_insert(self):
        root = ast.parse(open('test.py').read())
        ast.dump(root)
        print(root.body[0])




if __name__ == 'main':
    main()
