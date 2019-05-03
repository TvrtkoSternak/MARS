import ast

import astunparse
import git

from mars.astutils import AstUtils


def compare_commits(a_commit, b_commit):
    diff_index = a_commit.diff(b_commit)
    print(diff_index)
    for diff_item in diff_index.iter_change_type('M'):
        a_blob = diff_item.a_blob.data_stream.read().decode('utf-8')
        b_blob = diff_item.b_blob.data_stream.read().decode('utf-8')
        a_classes = extract_functions(ast.parse(a_blob))
        b_classes = extract_functions(ast.parse(b_blob))
        for pair in pair_functions(a_classes, b_classes):
            print(astunparse.unparse(pair[0]), pair[1])


def extract_functions(node):
    return AstUtils.find_functions(node)


def pair_functions(a_classes, b_classes):
    pairs = []
    for class_name in a_classes.keys():
        for func_name in a_classes[class_name].keys():
            pairs.append((
                a_classes[class_name][func_name],
                b_classes[class_name][func_name]
            ))
    return pairs


repo = git.Repo("D:/DIPLOMSKI RAD/test")
commits_list = list(repo.iter_commits('pattern_generalisation'))

compare_commits(commits_list[4], commits_list[3])
# for i in range(len(commits_list)-1):
#     compare_commits(commits_list[i+1], commits_list[i])
