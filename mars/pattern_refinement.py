from abc import ABC, abstractmethod


class PatternRefiner:
    """
    This class is the main part of the pattern refinement process and is
    responsible for finding the closest two patterns in the database and
    generating a generalised one from them. This is a standalone class
    that encapsulates all the basic refining functionalities but the
    refining process can also be enhanced by using some of the offered
    optimisers.

    ...

    Attributes
    ----------
    context : DbContext
        Database where all the patterns are saved
    min_patterns : int
        Minumum amount of patterns that need to be saved in the database after refinement
    max_distance : int
        Maximum distance between patterns that can be used for generalisation
    optimiser : IOptimiser
        Optimiser that offers additional functionalities for the refinement process

    Methods
    -------
    public __init__(self, optimiser, min_patterns, max_distance)
        Initialises PatternRefiner object.
    public void refine(self)
        Method that starts the refinement process.
    public Pattern, Pattern void find_nearest_patterns(self)
        Finds the most similar patterns in the database.
    public void add_wildcards(self, first_pattern, second_pattern)
        Compares the EditScripts of two chosen Patterns and changes nodes
        determined by the algorithm in both Patterns to wildcard nodes. Takes
        two Pattern objects as input.
    public void add_uses(self, first_pattern, second_pattern)
        Compares the EditScripts of two chosen Patterns and changes nodes
        determined by the algorithm in both Patterns to use nodes.
    public void connect_wildcards_and_uses(self, first_pattern, second_pattern)
        Compares the ASTs of two chosen Patterns and determines which are the
        corresponding wildcard-use and connects them. The pattern inputs are changed
        in place and will be the same after this method, any of them can be used to
        save in the database.
    """
    def __init__(self, context, optimiser=None, min_pattern=1, max_pattern=float('inf')):
        """
        Initialises PatternRefiner object.

        Parameters
        ----------
        optimiser : IOptimiser, optional
            This object is used in the further steps of pattern refinement
            to offer additional options for different pattern refinement approaches.
            Default is None.
            If there is no optimiser, the optimisation process will be the most
            basic one that PatternRefiner object provides as a standalone class.
        min_patterns : int, optional
            Used to limit the number of patterns that the PatternRefiner will generalise.
            Default is 1.
            If there is less or equal number of patterns in the database than min_patterns,
             the refinement process ends.
        max_distance : int, optional
            Used to determine the minimum similarity between the closest patterns in
            the database that can be refined.
            Default is inf.
            If all pattern similarities are greater than max_distance, the refinement process
            ends.
        """
        self.context = context
        self.optimiser = optimiser
        self.min_pattern = min_pattern
        self.max_pattern = max_pattern

    def refine(self):
        """
        Method that starts the refinement process.
        """
        pass

    def find_nearest_patterns(self):
        """
        Finds the most similar patterns in the database.

        Returns
        -------
        Pattern, Pattern
            Tuple of two most similar patterns in the database
        """
        pass

    def add_wildcards(self, first_pattern, second_pattern):
        """
        Compares the EditScripts of two chosen Patterns and changes nodes determined
        by the algorithm in both Patterns to wildcard nodes. Takes two Pattern objects
        as input.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass

    def add_uses(self, first_pattern, second_pattern):
        """
        Compares the EditScripts of two chosen Patterns and changes nodes
        determined by the algorithm in both Patterns to use nodes.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass

    def connect_wildcards_and_uses(self, first_pattern, second_pattern):
        """
        Compares the ASTs of two chosen Patterns and determines which are the
        corresponding wildcard-use and connects them. The pattern inputs are changed
        in place and will be the same after this method, any of them can be used to
        save in the database.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass


class IOptimiser(ABC):
    """
    This interface is a representation of classes used for optimisation
    of EditScripts and is used by the PatternRefiner class in the process
    of pattern refinement.

    ...

    Methods
    -------
    public void optimise(self, first_pattern, second_pattern)
        This method takes two Patterns and optimises their ChangeScripts in place.
    """

    @abstractmethod
    def optimise(self, first_pattern, second_pattern):
        """
        This method takes two Patterns and optimises their ChangeScripts in place.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass


class EditScriptOptimiser(IOptimiser):
    """
    This is a dummy class implementation of IOptimiser interface, it
    is initialised in the PatternRefiner class when we don’t want to
    use any advanced optimisation techniques on the change scripts.

    ...

    Methods
    -------
    public void __init__(self)
        Initialises EditScriptOptimiser object.
    public void optimise(self, first_pattern, second_pattern)
        This method is a dummy method, does not change the patterns at all.
    """

    def __init__(self):
        """
        Initialises EditScriptOptimiser object
        """
        pass

    def optimise(self, first_pattern, second_pattern):
        """
        This method is a dummy method, does not change the patterns at all.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass


class EditScriptOptimiserDecorator(IOptimiser):
    """
    This is a decorator class that is used to chain different change
    script optimisers that implement IOptimiser interface.

    ...

    Attributes
    ----------
    base_optimiser : IOptimiser
        Optimiser that is chained to this optimiser

    Methods
    -------
    public __init__(self, base_optimiser)
        Initialises BaseOptimiser object.
    public void optimise(self, first_pattern, second_pattern)
        This method takes two Patterns and optimises their ChangeScripts in place.
        After its optimisation, calls the optimise method of the next optimiser in chain.
    """

    def __init__(self, base_optimiser):
        """
        Initialises BaseOptimiser object.

        Parameters
        ----------
        base_optimiser : IOptimiser
            Optimiser that is chained to this optimiser
        """
        pass

    @abstractmethod
    def optimise(self, first_pattern, second_pattern):
        """
        This method takes two Patterns and optimises their ChangeScripts in place.
        After its optimisation, calls the optimise method of the next optimiser in chain.

        Parameters
        ----------
        first_pattern : Pattern
            Pattern that is chosen for refinement
        second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass


class ChangeIsolator(EditScriptOptimiserDecorator):
    """
    This class is a concrete implementation of IOptimiser interface.

    ...

    Attributes
    ----------
    base_optimiser : IOptimiser
        Optimiser that is chained to this optimiser

    Methods
    -------
    private void __isolate(self)
        This method is used for isolating important changes in ChangeScript objects.
    public void optimise(self, first_pattern, second_pattern)
        This method takes two Patterns and optimises their ChangeScripts in place.
        This concrete implementation aims to isolate the relevant changes in edit
        scripts of patterns so that they wouldn’t be replaced by wildcards in the
        next steps.
        After its optimisation, calls the optimise() method of the next optimiser in chain.
    """

    def optimise(self, first_pattern, second_pattern):
        """
        This method takes two Patterns and optimises their ChangeScripts in place.
        This concrete implementation aims to isolate the relevant changes in edit
        scripts of patterns so that they wouldn’t be replaced by wildcards in the
        next steps.
        After its optimisation, calls the optimise() method of the next optimiser in chain.

        Parameters
        ----------
            first_pattern : Pattern
            Pattern that is chosen for refinement
            second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass

    def __isolate(self):
        """
        This method is used for isolating important changes in ChangeScript objects.
        """
        pass


class MatchInserter(EditScriptOptimiserDecorator):
    """
    This class is a concrete implementation of IOptimiser interface.

    ...

    Attributes
    ----------
    base_optimiser : IOptimiser
        Optimiser that is chained to this optimiser

    Methods
    -------
    private void __insert(self)
        This method is used for inserting matches into the ChangeScript objects
    public void optimise(self, first_pattern, second_pattern)
        This method takes two Patterns and optimises their ChangeScript objects in place.
        This concrete implementation aims to recognise and locate matches between pattern
        change scripts so that generalisation of them would be maximised.
        After its optimisation, call the optimize method of the next optimiser in chain.
    """

    def optimise(self, first_pattern, second_pattern):
        """
        This method takes two Patterns and optimises their ChangeScript objects in place.
        This concrete implementation aims to recognise and locate matches between pattern
        change scripts so that generalisation of them would be maximised.
        After its optimisation, call the optimize method of the next optimiser in chain.

        Parameters
        ----------
            first_pattern : Pattern
            Pattern that is chosen for refinement
            second_pattern : Pattern
            Pattern that is chosen for refinement
        """
        pass

    def __insert(self):
        """
        This method is used for inserting matches into the ChangeScript objects.
        """
        pass
