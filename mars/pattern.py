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
        Returns change operation in a human-readable form

        Returns
        -------
            string
            Human-readable interpretation of ChangeOperation
        """
        pass


class Insert(ChangeOperation):

    def __init__(self, index, change):
        self.index = index
        self.change = change

    def make_change(self, original):
        pass

    def __str__(self):
        pass
