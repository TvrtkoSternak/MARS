from abc import ABC, abstractmethod
import ast


class Pattern:
    """
    A class used to represent patterns created by the system

    ...

    Attributes
    ----------
    original : ast
        AST of original code
    modified : ast
        AST of modified code
    edit_script : EditScript
        EditScript object that describes how to transform the original AST to modified AST

    Methods
    -------
    __init__(self, original, modified, edit_script)
        Initialises Pattern object.
    """
    def __init__(self, original, modified, node_pairs):
        """
        Initialises Pattern object

        Parameters
        ----------
        original : ast
            AST of original code
        modified : ast
            AST of modified code
        edit_script : EditScript
            EditScript object that describes how to transform the original AST to modified AST
        """
        self.original = original
        self.modified = modified
        self.node_pairs = node_pairs


class EditScript:
    """
    A class that represents a collection of operations which, when executed, change the original AST to modified AST

    ...

    Attributes
    ----------
    changes : list of ChangeOperation
        List  that  contains  all  change operations  that  need  to  be  executed  on  original  AST  to transform
        it to modified AST. Change operations are ordered by their execution priority (it is not guaranteed that the
        different execution order of change operations  will result with the correct modified AST)

    Methods
    -------
    __init__(self, original, modified, edit_script)
        Initialises EditScript object
    __iter__(self)
        Creates the Iterator object
    __next__(self)
        Returns the next ChangeOperation object in changes
    get(self, index)
        Returns ChangeOperation object at the specified index in changes
    add(self, change)
        Adds the specified ChangeOperation in changes
    """
    def __init__(self, changes=list()):
        """
        Initialises EditScript object

        Parameters
        ----------
        changes : list of ChangeOperation
            List that contains change operations(default is empty list)
        """
        self.changes = sorted(changes, key=lambda x: x.index, reverse=False)

    def __iter__(self):
        """
        Creates the Iterator object

        Returns
        -------
        Iterator
            Iterator object that iterates through changes
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Returns the next ChangeOperation object in changes

        Returns
        -------
        ChangeOperation
            The next ChangeOperation in changes list
        """
        if self.index >= len(self.changes):
            raise StopIteration
        self.index += 1
        return self.changes[self.index - 1]

    def get(self, index):
        """
        Returns ChangeOperation object at the specified index in changes

        Parameters
        ----------
        index : int
            Index of change operation in changes that the user wishes to retrieve

        Returns
        -------
        ChangeOperation
            ChangeOperation at the specified index

        Raises
        ------
        IndexError
            If the specified index is out of range
        """
        if index >= len(self.changes):
            raise IndexError('change index out of range')
        return self.changes[index]

    def add(self, change):
        """
        Adds the specified ChangeOperation in changes

        Parameters
        ----------
        change : ChangeOperation
            ChangeOperation to be added in changes
        """
        self.changes.append(change)
        self.changes.sort(key=lambda x: x.index, reverse=False)


class ChangeOperation(ABC):
    """
    A class that represents the operations used to transform the original code to modified code.

    ...

    Methods
    -------
    make_change(self, original)
        Applies the change operation to the received AST.
    __str__(self)
        Returns change operation in a human-readable form.
    """

    @abstractmethod
    def make_change(self, original_list_of_nodes):
        pass

    @abstractmethod
    def __str__(self):
        """
        Returns change operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of ChangeOperation
        """
        pass


class Insert(ChangeOperation):
    """
    A class that implements the insert change operation logic. It contains index of the node in the original AST where
    insert operation should be applied. It also contains AST that should be inserted at that position.

    ...

    Attributes
    ----------
    index : int
        Index of the node where insert operation should be applied
    change : ast
        AST of inserted code

    Methods
    -------
    __init__(self, index, change)
        Initialises Insert object.
    make_change(self, ast)
        Applies the insert operation to the received AST.
    """

    def __init__(self, index, change):
        """
        Initialises Insert object.

        Parameters
        ----------
        index : int
            Index of the node
        change : ast
            AST of inserted code
        """
        self.index = index
        self.change = change

    def make_change(self, original_list_of_nodes):
        """
        Applies the insert operation to the received AST.

        Parameters
        ----------
        original : ast
            AST of original code

        Returns
        -------
        ast
            Modified AST

        Raises
        IndexError
            If the specified index is out of range
        """
        original_list_of_nodes[self.index:self.index] = self.change.walk()
        return original_list_of_nodes

    def __str__(self):
        """
        Returns insert operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Insert
        """
        return "Insert operation @index " + str(self.index)

class Delete(ChangeOperation):
    """
    A class that implements the delete change operation logic. It deletes the node from AST at the specified index.

    ...

    Attributes
    ----------
    index : int
        Index of the node that should be deleted

    Methods
    -------
    __init__(self, index)
        Initialises Delete object.
    make_change(self, ast)
        Applies the delete operation to the received AST.
    """

    def __init__(self, index):
        """
        Initialises Delete object.

        Parameters
        ----------
        index : int
            Index of the node
        """

        self.index = index

    def make_change(self, original_list_of_nodes):
        """
        Applies the delete operation to the received AST.

        Parameters
        ----------
        original : ast
            AST of original code

        Returns
        -------
        ast
            Modified AST

        Raises
        IndexError
            If the specified index is out of range
        """
        end_index = original_list_of_nodes[self.index].num_children() + self.index + 1
        del original_list_of_nodes[self.index:end_index]
        return original_list_of_nodes

    def __str__(self):
        """
        Returns delete operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Delete
        """
        return "Delete operation @index " + str(self.index)


class Update(ChangeOperation):
    """
    A class that implements the update change operation logic. It wraps a combination of an Insert operation and Delete
    operation into one.

    ...

    Attributes
    ----------
    insert_operation : Insert
        Insert operation that should be executed as a part of update
    delete_operation: Delete
        Delete operation that should be executed as a part of update

    Methods
    -------
    __init__(self, index, change)
        Initialises Update object. It creates the Insert and Delete operation from received arguments.
    make_change(self, ast)
        Applies the update operation to the received AST.
    """

    def __init__(self, index, change):
        """
        Initialises Update object. It creates the Insert and Delete operation from received arguments.

        Parameters
        ----------
        index : int
            Index of the node that should be updated
        change : ast
            AST of updated code
        """
        self.index = index
        self.change = change

    def make_change(self, original_list_of_nodes):
        """
        Applies the update operation to the received AST.

        Parameters
        ----------
        original : ast
            AST of original code

        Returns
        -------
        ast
            Modified AST

        Raises
        IndexError
            If the specified index is out of range
        """
        end_index = original_list_of_nodes[self.index].num_children() + self.index + 1
        del original_list_of_nodes[self.index:end_index]
        original_list_of_nodes[self.index:self.index] = self.change.walk()
        return original_list_of_nodes

    def __str__(self):
        """
        Returns update operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Update
        """
        return "Update operation @index " + str(self.index)
