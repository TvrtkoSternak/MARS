from abc import ABC, abstractmethod


class Reader(ABC):
    """
    This class corresponds to the Subject role in Observer pattern. It contains the collection of IListener objects and
    methods for adding/removing them, along with the ability to notify them about change.

    ...

    Attributes
    ----------
    listeners : list of IListener
        List of observers that are listening for changes

    Methods
    -------
    public void notify(self)
        Notifies all subscribed listeners about change.
    public void subscribe(self, listener)
        Adds the received IListener object to the list of subscribed listeners.
    public void unsubscribe(self,listener)
        Removes the received IListener object from the list of subscribed listeners.
    """

    @abstractmethod
    def notify(self):
        """
        Notifies all subscribed listeners about change
        """
        pass

    @abstractmethod
    def subscribe(self, listener):
        """
        Adds the received IListener object to the list of subscribed listeners

        Parameters
        ----------
        listener : IListener
            IListener to subscribe
        """
        pass

    @abstractmethod
    def unsubscribe(self, listener):
        """
        Removes the received IListener object from the list of subscribed listeners

        Parameters
        ----------
        listener: IListener
            IListener to unsubscribe
        """
        pass


class Recommender(Reader):
    """
    This class corresponds to the Concrete Subject role in Observer pattern. Recommender is the core class which extends
    Reader class. This object is the “keeper” of the uploaded code in the form of AST. Its responsibility is iterating
    through the nodes and notifying all attached observers about the change of current node and requesting checking for
    matches. Once all the nodes have been visited it returns the found recommendations. The found patterns can be parsed
    into arbitrary format by providing appropriate IPatternParser object when instantiating Recommender object.

    ...

    Attributes
    ----------
    listeners : list of IListener
        List of observers that are listening for changes
    uploaded_ast : ast
        AST of the code that needs to be matched
    parser : IPatternParser
        Parser used for parsing found matches into understandable format

    Methods
    -------
    public __init__(self, parser)
        Initialises Recommender object.
    public void notify(self)
        Notifies all subscribed listeners about change.
    public void subscribe(self, listener)
        Adds the received IListener object to the list of subscribed listeners.
    public void unsubscribe(self,listener)
        Removes the received IListener object from the list of subscribed listeners.
    public File get_recommendations(self)
        Finds the matches for uploaded code block and returns file with recommendations.
    public void parse(self, pattern_matcher)
        Parses the IPatternMatcher object into the format determined by the parser.
    """

    def __init__(self, parser):
        """
        Initialises Recommender object

        Parameters
        ----------
        parser : IPatternParser
            Parser object for parsing matches
        """
        self.parser = parser

    def notify(self):
        """
        Notifies all subscribed listeners about change
        """
        pass

    def subscribe(self, listener):
        """
        Adds the received IListener object to the list of subscribed listeners

        Parameters
        ----------
        listener : IListener
            IListener to subscribe
        """
        pass

    def unsubscribe(self, listener):
        """
        Removes the received IListener object from the list of subscribed listeners

        Parameters
        ----------
        listener: IListener
            IListener to unsubscribe
        """
        pass

    def get_recommendations(self):
        """
        Finds the matches for uploaded code block and returns file with recommendations

        Returns
        -------
        File
            File with found recommendations
        """
        pass

    def parse(self, pattern_matcher):
        """
        Parses the IPatternMatcher object into the format determined by the parser

        Parameters
        ----------
        pattern_matcher: IPatternMatcher
            IPatternMatcher to be parsed
        """
        pass


