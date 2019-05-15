from pytz import unicode

a = dict()
b = 'str'
if isinstance(a, dict):
    print(a)
if isinstance(b, str) or isinstance(b, unicode):
    print(b)
