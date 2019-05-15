letters = list()
letters.append('a')
letters.append('b')
letters.append('c')
try:
    return is_vowel(letters[i])
except IndexError:
    raise Exception