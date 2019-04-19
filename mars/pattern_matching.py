from abc import ABC, abstractmethod
from .pattern import Pattern


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

    def __init__(self):
        self.listeners = []

    def notify(self):
        """
        Notifies all subscribed listeners about change
        """
        for listener in self.listeners:
            listener.update()

    def subscribe(self, listener):
        """
        Adds the received IListener object to the list of subscribed listeners

        Parameters
        ----------
        listener : IListener
            IListener to subscribe
        """
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        """
        Removes the received IListener object from the list of subscribed listeners

        Parameters
        ----------
        listener: IListener
            IListener to unsubscribe
        """
        self.listeners.remove(listener)


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
    public void get_present_node(self)
        Used by listeners to get information about recommender position in source ast.
    """

    def __init__(self, parser, source):
        """
        Initialises Recommender object

        Parameters
        ----------
        parser : IPatternParser
            Parser object for parsing matches
        source : String
            Source code of uploaded code ready for matching
        """
        super().__init__()
        self.parser = parser
        # TODO: Parse source to uploaded ast !!PREORDER!!
        self.uploaded_ast = []
        self.present_node = None

    def get_recommendations(self):
        """
        Finds the matches for uploaded code block and returns file with recommendations

        Returns
        -------
        File
            File with found recommendations
        """
        for node in self.uploaded_ast:
            self.present_node = node
            self.notify()

    def parse(self, pattern_matcher):
        """
        Parses the IPatternMatcher object into the format determined by the parser

        Parameters
        ----------
        pattern_matcher: IPatternMatcher
            IPatternMatcher to be parsed
        """
        self.parser.parse(pattern_matcher)

    def get_present_node(self):
        """
        Used by listeners to get information about recommender position in source ast

        Returns
        -------
        DetailedNode
            Node of ast thar the recommender is observing
        """
        return self.present_node


class IListener(ABC):
    """
    This class corresponds to the Observer role in theObserver design pattern.

    ...

    Methods
    -------
    public void update(self)
        Performs the appropriate update operation for the concrete implementation
    public void subscribe(self, reader)
        Subscribes the listener to Reader object
    public void unsubscribe(self)
        Unsubscribes the Listener from the reader object
    """

    @abstractmethod
    def update(self):
        """
        Performs the appropriate update operation for the concrete implementation
        """
        pass

    @abstractmethod
    def subscribe(self, reader):
        """
        Subscribes the listener to Reader

        Parameters
        ----------
        reader : Reader
            Reader object that the listener will subscribe to
        """
        pass

    @abstractmethod
    def unsubscribe(self):
        """
        Unsubscribes the Listener from the reader object
        """


class IPatternFactory(ABC):
    """
    This class describes classes that are used for creating IPatternMatcher objects. When the factory finds a match, it
    creates all patterns that start with the found match.

    ...

    Methods
    -------
    public IPatternMatcher create_pattern(self)
        Creates IPatternMatcher object for the detected pattern.
    """

    @abstractmethod
    def create_pattern(self):
        """
        Creates and returns IPatternMatcher object for the detected pattern.

        Returns
        -------
        IPatternMatcher
            IPatternMatcher that   contains   a   Pattern   that the   concrete   factory   is responsible for creating.
        """
        pass


class IPatternMatcher(ABC):
    """
    This class is responsible for checking if two patterns match.

    ...

    Attributes
    ----------
    pattern : Pattern
        Pattern  object  that  is  being  checked  against  incoming  patterns  for matches
    wildcard_matches : list of ast
        List of ASTs that were matched to wildcard nodes in the IPatternMatcher Pattern object. Used later in parsing of
        the matched patterns.

    Methods
    -------
    public __init__(pattern)
        Initialises IPatternMatcher with pattern to match
    public bool check_match(self, node)
        Check if the input node matches the IPatternMatcher node that is next in the pattern.
    """

    def __init__(self, pattern):
        """
        Initialises IPatternMatcher with pattern to match
        Parameters
        ----------
        pattern : Pattern
            Pattern  object  that  is  being  checked  against  incoming  patterns  for matches
        """
        self.pattern = pattern

    @abstractmethod
    def check_match(self, node):
        """
        Check if the input node matches the IPatternMatcher node that is next in the pattern.

        Parameters
        node: ast
            AST node that is checked for match in next IPatternMatcher Pattern node

        Returns
        bool
            True if the nodes match, false otherwise
        """
        pass


class PatternFactoryListener(IPatternFactory, IPatternMatcher, IListener):
    """
    This  class corresponds  to  the  Concrete Observer  role  in  the  Observer  design  pattern.  It  inherits from
    IListener, IPatternMatcher and IPatternFactory. It is used for creating PatternListener objects. When update is
    called it retrieves the current node from Recommender and checks for match. If the match is found, appropriate
    PatternListener is created and subscribed to Recommender.

    ...

    Attributes
    ----------
    recommender : Recommender
        Recommender object that the listener is listening to
    pattern: Pattern
        IPatternMatcher  own  Pattern  object  that  is  being  checked  against  incoming  patterns  for matches
    wildcard_matches: list of ast
        List of ASTs that were matched to wildcard nodes in the IPatternMatcher Pattern object. Used later in parsing of
        the matched patterns.

    Methods
    -------
    public void update(self)
        Method called by the Reader class. When this method is called PatternFactoryListener object retrieves the
        current node from Recommender and checks for match, if the node matches then the PatternFactoryListener creates
        a designated PatternListener.
    public void create_pattern(self):
        Creates and returns IPatternMatcher object for the detected pattern.
    public bool check_match(self, node):
        Check if the input node matches the IPatternMatcher node that is next in the pattern.
    public void subscribe(self, reader)
        Subscribes the listener to Reader object
    public void unsubscribe(self)
        Removes itself from the list of listeners in the associated Reader object.
    """

    def update(self):
        """
        Method called by the Reader class. When this method is called PatternFactoryListener object retrieves the
        current node from Recommender and checks for match, if the node matches then the PatternFactoryListener creates
        a designated PatternListener.
        """
        pass

    def create_pattern(self):
        """
        Creates and returns IPatternMatcher object for the detected pattern.

        Returns
        -------
        IPatternMatcher
            IPatternMatcher that contains a Pattern that the concrete factory is responsible for creating
        """
        pass

    def check_match(self, node):
        """
        Check if the input node matches the IPatternMatcher node that is next in the pattern.

        Parameters
        ----------
        node : ast
            AST node that is checked for match in next IPatternMatcher Pattern node

        Returns
        -------
        bool
            True if the nodes match, false otherwise
        """
        pass

    def subscribe(self, reader):
        """
        Subscribes the PatternFactoryListener to Reader

        Parameters
        ----------
        reader : Reader
            Reader object that the PatternFactoryListener will subscribe to
        """
        pass

    def unsubscribe(self):
        """
        Removes itself from the list of listeners in the associated Reader object.
        """
        pass


class PatternListener(IListener, IPatternMatcher):
    """
    This class corresponds to the Concrete Observer role in the Observer design pattern. It inherits from IListener and
    IPatternMatcher. When the current node in Reader changes this class checks if the now new current node matches with
    the pattern. If it does match, it goes on with checking. If it does not, it removes itself from the list of
    listeners in the Reader.

    ...

    Attributes
    ----------
    recommender : Recommender
        Recommender object that the listener is listening to
    pattern : Pattern
        IPatternMatcher  own  Pattern  object  that  is  being  checked  against  incoming  patterns for matches
    wildcard_matches : list of ast
        List of ASTs that were matched to wildcard nodes in the IPatternMatcher Pattern object. Used later in parsing of
        the matched patterns
    index : int
        Index of the last checked node

    Methods
    -------
    public void update(self)
        Method called by the Reader class. When this method is called PatternListener object retrieves the current node
        from Recommender and checks for match. If the node is not a match, then PatternListener unsubscribes from the
        Reader.
        If the pattern is a match there are two scenarios:
        1) The matched node is the last node in the Pattern:
            Pattern listener unsubscribes from the reader and requests parsing.
        2) The matched node is not the last node in the pattern:
            Pattern listener increments its internal node count and continues to listen for updates from the reader.
    public void create_pattern(self)
        Creates and returns IPatternMatcher object for the detected pattern.
    public bool check_match(self, node)
        Check if the input node matches the IPatternMatcher node that is next in the pattern.
    public void subscribe(self, reader)
        Subscribes the listener to Reader object
    public void unsubscribe(self)
        Removes itself from the list of listeners in the associated Reader object.
    """

    def update(self):
        """
        Method called by the Reader class. When this method is called PatternListener object retrieves the current node
        from Recommender and checks for match. If the node is not a match, then PatternListener unsubscribes from the
        Reader.
        If the pattern is a match there are two scenarios:
        1) The matched node is the last node in the Pattern:
            Pattern listener unsubscribes from the reader and requests parsing.
        2) The matched node is not the last node in the pattern:
            Pattern listener increments its internal node count and continues to listen for updates from the reader.
        """
        pass

    def check_match(self, node):
        """
        Check if the input node matches the IPatternMatcher node that is next in the pattern.

        Parameters
        ----------
        node : ast
            AST node that is checked for match in next IPatternMatcher Pattern node

        Returns
        -------
        bool
            True if the nodes match, false otherwise
        """
        pass

    def subscribe(self, reader):
        """
        Subscribes the PatternListener to Reader

        Parameters
        ----------
        reader : Reader
            Reader object that the PatternListener will subscribe to
        """
        pass

    def unsubscribe(self):
        """
        Removes itself from the list of listeners in the associated Reader object.
        """
        pass