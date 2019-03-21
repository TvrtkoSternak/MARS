from abc import ABC, abstractmethod


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
    def __init__(self, original, modified, edit_script):
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
        self.edit_script = edit_script


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
    def __init__(self, changes=None):
        """
        Initialises EditScript object

        Parameters
        ----------
        changes : list of ChangeOperation
            List that contains change operations(default is None)
        """

        self.changes = changes

    def __iter__(self):
        """
        Creates the Iterator object

        Returns
        -------
        Iterator
            Iterator object that iterates through changes
        """

        pass

    def __next__(self):
        """
        Returns the next ChangeOperation object in changes

        Returns
        -------
        ChangeOperation
            The next ChangeOperation in changes list
        """

        pass

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

        pass

    def add(self, change):
        """
        Adds the specified ChangeOperation in changes

        Parameters
        ----------
        change : ChangeOperation
            ChangeOperation to be added in changes
        """

        pass


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
    def make_change(self, original):
        """
        Applies the change operation to the received AST.

        Parameters
        ----------
        original : ast
            AST of original code

        Returns
        -------
        ast
            Modified AST
        """
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

    def make_change(self, original):
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
        pass

    def __str__(self):
        """
        Returns insert operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Insert
        """
        pass


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

    def make_change(self, original):
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
        pass

    def __str__(self):
        """
        Returns delete operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Delete
        """
        pass


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

        pass

    def make_change(self, original):
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
        pass

    def __str__(self):
        """
        Returns update operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Update
        """
        pass


class Move(ChangeOperation):
    """
    A  class  that  implements  the  move  change  operation  logic.  It  combines  the  delete  and  insert operation
    in a way that it deletes the AST node at first index and then inserts the deleted AST node at the second index.

    ...

    Attributes
    ----------
    insert_operation : Insert
        Insert operation that should be executed as a part of move
    delete_operation: Delete
        Delete operation that should be executed as a part of move

    Methods
    -------
    __init__(self, insert_index, delete_index)
        Initialises Move object. It creates Insert and Delete operations which combined implement move logic.
    make_change(self, ast)
        Applies the move operation to the received AST.
    """

    def __init__(self, insert_index, delete_index):
        """
        Initialises Move object. It creates Insert and Delete operations which combined implement move logic.

        Parameters
        ----------
        insert_index : int
            The position in the AST to which node needs to be moved
        delete_index : ast
            The position of the AST node that needs to be moved
        """

        pass

    def make_change(self, original):
        """
        Applies the move operation to the received AST.

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
        pass

    def __str__(self):
        """
        Returns move operation in a human-readable form.

        Returns
        -------
        string
            Human-readable interpretation of Move
        """
        pass
