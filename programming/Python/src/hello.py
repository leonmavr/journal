class Bar:
    """
    Bar's doc
    """
    def __init__(self, i):
        Bar._i = i
        
def foo():
    """
    foo's doc
    """
    i = 0
    return "foo"