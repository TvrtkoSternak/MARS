import copy
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

import astunparse

from mars.astwrapper import Use
from mars.pattern import Update, EditScript


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
    def __init__(self):
        self.recommendation = ''
        self.recommendations = list()

    def parse(self, pattern_matcher):
        """
        Parses the IPatternMatcher into a human-readable form and writes it to
        standard output.

        Parameters
        ----------
        pattern_matcher : IPatternMatcher
            IPatternMatcher object that will be parsed and written to standard
            output
        """
        edit_operations = list()
        list_pattern_matcher_copy = copy.deepcopy(pattern_matcher.pattern.modified.walk())

        for index, node in enumerate(list_pattern_matcher_copy):
            if isinstance(node, Use):
                wildcard_block = list()
                while pattern_matcher.wildcard_blocks[node.index]:
                    wildcard_block.append(pattern_matcher.wildcard_blocks[node.index].pop(0).reconstruct(pattern_matcher.wildcard_blocks[node.index]))
                edit_operations.append(Update(index, wildcard_block))

        edit_script = EditScript(edit_operations)
        edit_script.execute(list_pattern_matcher_copy)

        pattern = list_pattern_matcher_copy.pop(0).reconstruct(list_pattern_matcher_copy)
        self.recommendation += pattern.to_source_code(0)
        self.recommendations.append((pattern_matcher.no_line, pattern.to_source_code(0)))

    def get_recommended_code(self):
        current_line = 1
        self.recommendations.sort(key=lambda tup: tup[0])
        code = list()
        for recommendation in self.recommendations:
            while current_line < recommendation[0]:
                code.insert(current_line, "")
                current_line += 1
            position = recommendation[0]
            for line in recommendation[1].split("\n"):
                if len(code) > position:
                    tab = code[position-1].replace("    ", "\t").count('\t')
                    code[position-1] = ("    "*tab)+line.replace("\t", "")
                else:
                    code.insert(position, line)
                position += 1
            current_line = position
        return '\n'.join(code)

    def clear(self):
        self.recommendation = ''
        self.recommendations.clear()


class CounterPatternParser(PatternParser):
    def __init__(self):
        self.counter = 0

    def parse(self, pattern_matcher):
        self.counter += 1

    def get_count(self):
        return self.counter
