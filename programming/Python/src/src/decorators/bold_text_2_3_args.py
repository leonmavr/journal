def make_bold2(func):
    """HOF - augments a function of 2 arguments"""
    tag_beg, tag_end = '<b>', '</b>'
    def inner(word1: str, word2: str):
        return '{}{}{}'.format(tag_beg, func(word1, word2), tag_end)
    return inner

def make_bold3(func):
    """HOF - augments a function of 3 arguments"""
    tag_beg, tag_end = '<b>', '</b>'
    def inner(word1: str, word2: str, word3: str):
        return '{}{}{}'.format(tag_beg, func(word1, word2, word3), tag_end)
    return inner

def join2(word1: str, word2: str):
    """Dummy function that we want to augment, i.e. pass in a HOF"""
    return word1 + word2

def join3(word1: str, word2: str, word3: str):
    """Dummy function that we want to augment, i.e. pass in a HOF"""
    return word1 + word2 + word3

bold = make_bold2(join2)
print(bold('A ', 'quick'))
bold = make_bold3(join3)
print(bold('brown ', 'fox ', 'jumps'))
