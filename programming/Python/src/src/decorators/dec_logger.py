import sys


def log_to_file(fname = '/tmp/log.txt'):
    def log_to_file_inner(func):
        sys.stdout = sys.stderr = open(fname, 'a')
        def inner(*args):
            func(*args)
        return inner
    return log_to_file_inner


@log_to_file(fname = '/tmp/log_test1.txt')
def print_table(text: str):
    n = len(text)
    print('-'*(n+4))
    print('| ' + text +  ' |')
    print('-'*(n+4))

print_table('Test 1 results')
