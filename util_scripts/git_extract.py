import ast

import astunparse
import git


def compare_commits(a_commit, b_commit):
    diff_index = a_commit.diff(b_commit)
    print(diff_index)
    print(ast.parse("string").body[0].value)
    for diff_item in diff_index.iter_change_type('M'):
        print(diff_item)
        a_blob = diff_item.a_blob.data_stream.read().decode('utf-8')
        b_blob = diff_item.b_blob.data_stream.read().decode('utf-8')
        #print(astunparse.unparse(ast.parse(b_blob).body[1].body[1]))
        #print(ast.parse(b_blob).body[1].body[1].body[0].value)


repo = git.Repo("D:/DIPLOMSKI RAD/test")
commits_list = list(repo.iter_commits('pattern_generalisation'))

for i in range(len(commits_list)-1):
    compare_commits(commits_list[i+1], commits_list[i])
