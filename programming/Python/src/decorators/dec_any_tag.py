def make_tag(tag = 'b'):
    def make_tag_inner(func):
        tag_beg, tag_end = '<{}>'.format(tag), '</{}>'.format(tag)
        def inner(*args):
            return '{}{}{}'.format(tag_beg, func(*args), tag_end)
        return inner
    return make_tag_inner

@make_tag('div')
def join2(word1: str, word2: str):
    """Function to decorate"""
    return word1 + word2

print(join2('brown ', 'fox '))
