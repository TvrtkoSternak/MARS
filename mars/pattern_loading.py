from abc import ABC, abstractmethod


class IPatternLoader(ABC):
    """
    This interface represents the classes used for loading the patterns from the database.

    ...

    Methods
    -------
    load(self)
        Loads all patterns from the database.
    """
    @abstractmethod
    def load(self):
        """
        Loads all patterns from the database.

        Returns
        -------
        list of IPatternMatcher
            List of all loaded patterns in the database
        """
        pass


class PatternLoader(IPatternLoader):
    """
    This class is responsible for loading available patterns from database.

    ...

    Attributes
    ----------
    context : DbContext
        Database where all the patterns are saved

    Methods
    -------
    public __init__(self, context)
        Initialises PatternLoader object.
    public list of IPatternMatcher load(self)
        Loads all the patterns available in the database and returns them
        as a list of IPatternMatcher objects.
    """
    def __init__(self, context):
        """
        Initialises PatternLoader object.

        Parameters
        ----------
        context : DbContext
            Database where all the patterns are saved
        """
        pass

    def load(self):
        """
        Loads all the patterns available in the database and returns
        them as a list of IPatternMatcher objects.

        Returns
        -------
        list of IPatternMatcher
            List of all loaded patterns
        """
        pass


class PatternFactoryLoader(IPatternLoader):
    """
    This class is responsible for loading pattern factories that are used
    for creating actual patterns.

    ...

    Attributes
    ----------
    context : DbContext
        Database where all the patterns are saved

    Methods
    -------
    public __init__(self, context)
        Initialises PatternFactoryLoader object.
    public list of IPatternMatcher load(self)
        Loads factories for all the patterns available
        in the database and returns them as a list of
        IPatternMatcher objects.
    """
    def __init__(self, context):
        """
        Initialises PatternFactoryLoader object.

        Parameters
        ----------
        context : DbContext
            Database where all the patterns are saved
        """
        pass

    def load(self):
        """
        Loads factories for all the patterns available in the
        database and returns them as a list of IPatternMatcher objects.

        Returns
        -------
        list of IPatternMatcher
            List of all loaded pattern factories
        """
        pass
