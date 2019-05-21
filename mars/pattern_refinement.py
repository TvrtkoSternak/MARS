from abc import ABC, abstractmethod

from mars.astutils import AstWrapper
from mars.astwrapper import Wildcard, Use, Function
from mars.pattern import Insert, Update, EditScript, Delete
from mars.pattern_creation import PatternCreator


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
    def __init__(self, context, edit_script_generator, optimiser=None, min_no_patterns=2, max_pattern_distance=float('inf')):
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
        self.min_no_patterns = min_no_patterns
        self.max_pattern_distance = max_pattern_distance
        self.edit_script_generator = edit_script_generator
        self.pattern_creator = PatternCreator(self.edit_script_generator.tree_differencer, AstWrapper())

    def refine(self):
        """
        Method that starts the refinement process.
        """
        patterns = self.context.load()

        while True:
            if len(patterns) <= max(self.min_no_patterns, 1):
                break

            first_pattern, second_pattern, distance = self.find_nearest_patterns(patterns)

            if distance >= self.max_pattern_distance:
                break

            wildcards = self.add_wildcards(first_pattern.original, second_pattern.original)
            uses = self.add_uses(first_pattern.modified, second_pattern.modified)
            wildcards, uses = self.connect_wildcards_and_uses(wildcards, uses,
                                            first_pattern.node_pairs, second_pattern.node_pairs)

            edit_script_wild = EditScript(wildcards)
            edit_script_use = EditScript(uses)

            list_org = first_pattern.original.walk()
            list_mod = first_pattern.modified.walk()

            edit_script_wild.execute(list_org)
            edit_script_use.execute(list_mod)

            # reconstructed_org = list_org.pop(0).reconstruct(list_org)
            # reconstructed_mod = list_mod.pop(0).reconstruct(list_mod)
            #
            # list_reconstructed_org = reconstructed_org.walk()
            # list_reconstructed_mod = reconstructed_mod.walk()

            self.optimiser.optimise(list_org, list_mod)

            created_pattern = self.pattern_creator.create_pattern(list_org.pop(0).reconstruct(list_org),
                                                                  list_mod.pop(0).reconstruct(list_mod),
                                                                  patterns_wrapped=True)

            patterns.remove(first_pattern)
            patterns.remove(second_pattern)
            patterns.append(created_pattern)

        self.context.rewrite(patterns)

    def find_nearest_patterns(self, patterns):
        """
        Finds the most similar patterns in the database.

        Returns
        -------
        Pattern, Pattern
            Tuple of two most similar patterns in the database
        """
        pattern_pairs = dict()

        for i in range(0, len(patterns) - 1, 1):
            for j in range(i + 1, len(patterns), 1):
                pattern_pairs[(patterns[i], patterns[j])] = self.calculate_distance(patterns[i], patterns[j])

        min_pair = min(pattern_pairs, key=pattern_pairs.get)

        return min_pair[0], min_pair[1], pattern_pairs.get(min_pair, 0)

    def calculate_distance(self, first_pattern, second_pattern):
        original_edit_script = self.edit_script_generator.generate(first_pattern.original, second_pattern.original)
        modified_edit_script = self.edit_script_generator.generate(first_pattern.modified, second_pattern.modified)

        return original_edit_script.size(first_pattern.original) + modified_edit_script.size(first_pattern.modified)

    def add_wildcards(self, first_pattern_org, second_pattern_org):
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
        edit_script = self.edit_script_generator.generate(first_pattern_org, second_pattern_org)
        wildcards = dict()

        list_first_pattern = first_pattern_org.walk()

        offset = 0
        for operation in edit_script:
            if isinstance(operation, Insert):
                wildcards[operation.index] = Update(operation.index, Wildcard(operation.change, operation))
                print(operation.__class__)
                print(operation.change)
            else:
                wildcards[operation.index] = Update(operation.index, Wildcard(list_first_pattern[operation.index], operation))
                print(operation.__class__)
                if isinstance(operation, Delete):
                    offset += 1

        edit_operations = list()

        for value in wildcards.values():
            edit_operations.append(value)

        return edit_operations

        # edit_script_wildcards = EditScript(edit_operations)
        # list_first_pattern_copy = copy.deepcopy(list_first_pattern)
        # edit_script_wildcards.execute(list_first_pattern_copy)
        # return list_first_pattern_copy

    def add_uses(self, first_pattern_mod, second_pattern_mod):
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
        edit_script = self.edit_script_generator.generate(first_pattern_mod, second_pattern_mod)
        uses = dict()

        list_first_pattern = first_pattern_mod.walk()

        offset = 0
        for operation in edit_script:
            if isinstance(operation, Insert):
                uses[operation.index] = Update(operation.index, Use(operation.change, operation))
            else:
                uses[operation.index] = Update(operation.index, Use(list_first_pattern[operation.index], operation))
                if isinstance(operation, Delete):
                    offset += 1

        edit_operations = list()

        for value in uses.values():
            edit_operations.append(value)

        return edit_operations

        # edit_script_uses = EditScript(edit_operations)
        # list_first_pattern_copy = copy.deepcopy(list_first_pattern)
        # edit_script_uses.execute(list_first_pattern_copy)
        # return list_first_pattern_copy

    def connect_wildcards_and_uses(self, wildcards, uses, first_pattern_similarity_list, second_pattern_similarity_list):
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
        i = 1
        for wildcard in wildcards:
            if isinstance(wildcard.change.type, Insert):
                pair = next((key for key, value in second_pattern_similarity_list.items() if wildcard.change.wrapped_node in key), None)
            else:
                pair = next((key for key, value in first_pattern_similarity_list.items() if wildcard.change.wrapped_node in key), None)

            if pair:
                use = next((x for x in uses if x.change.wrapped_node in pair), None)
                if use:
                    wildcard.change.index = i
                    use.change.index = i
                    i += 1

        wildcards = [x for x in wildcards if x.change.index != 0]
        uses = [x for x in uses if x.change.index != 0]

        return wildcards, uses


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
        self.base_optimiser = base_optimiser

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


class WildcardUseCompressor(EditScriptOptimiserDecorator):
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

    def optimise(self, pattern_org, pattern_mod):
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
        self.base_optimiser.optimise(pattern_org, pattern_mod)
        matching_blocks_index_list = list()

        for i in range(0, len(pattern_org) - 1, 1):
            for j in range(0, len(pattern_mod) - 1, 1):
                if self.check_compatability(pattern_org[i], pattern_mod[j]) and self.check_compatability(pattern_org[i+1], pattern_mod[j+1]):
                    matching_blocks_index_list.append((i, j))

        edit_operations_org = list()
        edit_operations_mod = list()

        for index_org, index_mod in matching_blocks_index_list:
            edit_operations_org.append(Delete(index_org + 1))
            edit_operations_mod.append(Delete(index_mod + 1))

        edit_org = EditScript(edit_operations_org)
        edit_mod = EditScript(edit_operations_mod)

        edit_org.execute(pattern_org)
        edit_mod.execute(pattern_mod)

    def check_compatability(self, node_org, node_mod):
        return isinstance(node_org, Wildcard) and isinstance(node_mod, Use) and node_org.index == node_mod.index

class FunctionPropagator(EditScriptOptimiserDecorator):
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

    def optimise(self, pattern_org, pattern_mod):
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
        self.base_optimiser.optimise(pattern_org, pattern_mod)

        pattern_org_functions = [(index, node.value, [arg for arg in node.args]) for index, node in enumerate(pattern_org) if isinstance(node, Function)]
        pattern_mod_functions = [(index, node.value, [arg for arg in node.args]) for index, node in enumerate(pattern_mod) if isinstance(node, Function)]

        edit_operations_org = list()
        edit_operations_mod = list()

        for function_org in pattern_org_functions:
            for function_mod in pattern_mod_functions:
                if self.check_compatability(function_org[1], function_mod[1]) and self.arg_check(function_org[2], function_mod[2]):
                    wildcard = Wildcard(None, Update(0, None))
                    use = Use(None, Update(0, None))
                    wildcard.index = function_org[1].index
                    use.index = function_mod[1].index
                    edit_operations_org.append(Update(function_org[0], wildcard))
                    edit_operations_mod.append(Update(function_mod[0], use))

        edit_org = EditScript(edit_operations_org)
        edit_mod = EditScript(edit_operations_mod)

        edit_org.execute(pattern_org)
        edit_mod.execute(pattern_mod)

    def check_compatability(self, node_org, node_mod):
        return isinstance(node_org, Wildcard) and isinstance(node_mod, Use) and node_org.index == node_mod.index

    def arg_check(self, arg_org, arg_mod):
        if len(arg_org) == len(arg_mod):
            for arg1, arg2 in zip(arg_org, arg_mod):
                if not self.check_compatability(arg1, arg2):
                    return False

        return True
