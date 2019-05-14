import ast
from difflib import SequenceMatcher
from io import StringIO
import tokenize

import astunparse
import git

from mars.astutils import AstUtils


def compare_commits(a_commit, b_commit):
    diff_index = a_commit.diff(b_commit)
    accepted_commits = list()
    for diff_item in diff_index.iter_change_type('M'):
        a_blob = diff_item.a_blob.data_stream.read().decode('utf-8')
        b_blob = diff_item.b_blob.data_stream.read().decode('utf-8')
        try:
            a_classes = extract_functions(ast.parse(a_blob))
            b_classes = extract_functions(ast.parse(b_blob))
            for pair in pair_functions(a_classes, b_classes):
                if pair[0] is not None and pair[1] is not None:
                    try:
                        s = SequenceMatcher(None,
                                            unparse_function_body_and_remove_docstring(pair[0]),
                                            unparse_function_body_and_remove_docstring(pair[1]))
                        if s.ratio() < 1.0:
                            accepted_commits.append(pair)
                    except IOError:
                        print("exception in unparsing")
        except SyntaxError as e:
            print("exception in function extraction, syn err")
            print(str(e))

        return accepted_commits


def extract_functions(node):
    return AstUtils.find_functions(node)


def pair_functions(a_classes, b_classes):
    pairs = []
    for class_name in a_classes.keys():
        for func_name in a_classes[class_name].keys():
            try:
                pairs.append((
                    a_classes[class_name][func_name],
                    b_classes[class_name][func_name]
                ))
            except KeyError:
                print("func or class not found")
    return pairs

def unparse_function_body_and_remove_docstring(function):
    return astunparse.unparse(ast.parse(remove_comments_and_docstrings(astunparse.unparse(function))).body[0].body)

def remove_comments_and_docstrings(source):
    """
    Returns 'source' minus comments and docstrings.
    """
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out


repo = git.Repo("/home/tvrtko/Documents/Fer/MARS")
commits_list = list(repo.iter_commits('development'))
commits = list()
for i in range(len(commits_list)-1):
    returned_commits = compare_commits(commits_list[i+1], commits_list[i])
    if returned_commits is not None and returned_commits:
        commits.append(returned_commits)

print(len(commits))

