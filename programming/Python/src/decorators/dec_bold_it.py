def make_bold(func):
    """HOF - augments the `inner` function"""
    tag_beg, tag_end = '<b>', '</b>'
    def inner(*args):
        return '{}{}{}'.format(tag_beg, func(*args), tag_end)
    return inner

@make_bold
def join3(word1: str, word2: str, word3: str):
    """Function to decorate"""
    return word1 + word2 + word3

print(join3('brown ', 'fox ', 'jumps'))
