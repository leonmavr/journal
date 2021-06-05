def make_bold(func):
    """HOF - augments the `inner` function"""
    tag_beg, tag_end = '<b>', '</b>'
    def inner(*args):
        return '{}{}{}'.format(tag_beg, func(*args), tag_end)
    return inner

def join2(word1: str, word2: str):
    """Dummy function that we want to augment, i.e. pass in a HOF"""
    return word1 + word2

def join3(word1: str, word2: str, word3: str):
    """Dummy function that we want to augment, i.e. pass in a HOF"""
    return word1 + word2 + word3

bold = make_bold(join2)
print(bold('A ', 'quick'))
bold = make_bold(join3)
print(bold('brown ', 'fox ', 'jumps'))
