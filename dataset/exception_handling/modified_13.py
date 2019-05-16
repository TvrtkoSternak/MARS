try:
    let = letters[i]
except IndexError:
    raise Exception
else:
    return is_vowel(let)
