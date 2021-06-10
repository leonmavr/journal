import time

def memoize(func):
    cache = {}
    def inner(*args):
        if args not in cache:
            # register it in cache
            cache[args] = func(*args)
        return cache[args]
    return inner

@memoize
def long_function(n):
    dur = n*0.1
    time.sleep(dur)
    return dur

if __name__ == '__main__':
    before = time.time()
    for _ in range(1000):
        long_function(5)
    print("Took {:.4f} sec".format(time.time() - before))
