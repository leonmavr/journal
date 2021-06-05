def make_bold(func):
    """HOF that accepts a function `func` and returns a new one.
    The new function calls `func` and modifies its return value.
    That new function is returned."""
    tag_beg, tag_end = '<b>', '</b>'
    def inner(text: str):
        return '{}{}{}'.format(tag_beg, func(text), tag_end)
    return inner

def get_text(text: str):
    """Dummy function that we want to augment, i.e. pass it in a HOF"""
    return text

bold = make_bold(get_text)
print(bold('A quick brown fox'))
print(bold('jumps over the'))
