letters = list()
letters.append('a')
letters.append('b')
letters.append('c')
try:
    let = letters[i]
except IndexError:
    raise Exception
else:
    return is_vowel(let)
