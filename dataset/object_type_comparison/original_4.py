import types

a = dict()
b = 'str'
if type(a) is types.DictType:
    print(a)
if type(b) in types.StringTypes:
    print(b)
