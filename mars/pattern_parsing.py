from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

import astunparse


class PatternParser(ABC):
    """
    This interface is a representation of the classes used
    for parsing the patterns generated  by the system and
    patterns matched in the code.

    ...

    Methods
    -------
    public void parse(self, pattern_matcher)
        Parses the input pattern.
    """

    @abstractmethod
    def parse(self, pattern_matcher):
        """
        Parses the input pattern.

        Parameters
        ----------
        pattern_matcher : IPatternMatcher
            IPatternMatcher object that is being parsed by the IPatternParser
            concrete implementation
        """
        pass


class XMLPatternParser(PatternParser):
    """
    This class is responsible for parsing matched patterns into XML
    form which will be used by the web user interface to present the
    code analysis results. This parser writes to the file passed to it
    in its constructor.

    ...

    Attributes
    ----------
    output : File
        File in which the parser writes parsed patterns

    Methods
    -------
    public __init__(self, output)
        Initialises XMLPatternParser object.

    public void parse(self, pattern)
        Parses the IPatternMatcher into a XML form and writes it to a file.
    """

    def __init__(self, output):
        """
        Initialises XMLPatternParser object.

        Parameters
        ----------
        output : File
            File in which the parser will write the parsed patterns
        """
        self.output = output

    def parse(self, pattern_matcher):
        """
        Parses the IPatternMatcher into a XML form and writes it to a file.

        Parameters
        ----------
        pattern_matcher : IPatternMatcher
            IPatternMatcher object that will be parsed and written to a file
        """
        change = ET.Element('change')
        start = ET.SubElement(change, 'start')
        start.set('start_line', pattern_matcher.start_lineno)
        end = ET.SubElement(change, 'end')
        end.set('end_line', pattern_matcher.last_lineno)
        change_code = ET.SubElement(change, 'change_code')
        change_code.set('change_code', astunparse.unparse(pattern_matcher.pattern.modified))

        data = ET.tostring(change)
        self.output.write(data)


class ReadablePatternParser(PatternParser):
    """
    This class is responsible for parsing the patterns into a human-readable
    form so that the system can present the user all the patterns used in code
    analysis. This parser writes directly to the standard output so there is
    no additional context passed to it.

    ...

    Methods
    -------
    public void parse(self, pattern)
        Parses the IPatternMatcher into a human-readable form and writes
        it to standard output.
    """

    def parse(self, pattern):
        """
        Parses the IPatternMatcher into a human-readable form and writes it to
        standard output.

        Parameters
        ----------
        pattern : IPatternMatcher
            IPatternMatcher object that will be parsed and written to standard
            output
        """


class CounterPatternParser(PatternParser):
    def __init__(self):
        self.counter = 0

    def parse(self, pattern_matcher):
        self.counter += 1

    def get_count(self):
        return self.counter