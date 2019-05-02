import ast

import astunparse
import git

repo = git.Repo("D:/DIPLOMSKI RAD/test")
commits_list = list(repo.iter_commits('pattern_generalisation'))

a_commit = commits_list[2]
b_commit = commits_list[1]

diff_index = a_commit.diff(b_commit)
print(diff_index)
for diff_item in diff_index.iter_change_type('M'):
    print(diff_item)
    a_blob = diff_item.a_blob.data_stream.read().decode('utf-8')
    b_blob = diff_item.b_blob.data_stream.read().decode('utf-8')
    print(astunparse.unparse(ast.parse(b_blob).body[1].body[1]))
    print(ast.parse(b_blob).body[1].body[1].body[0].value)
