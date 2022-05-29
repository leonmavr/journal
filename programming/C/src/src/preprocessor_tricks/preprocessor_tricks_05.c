#include <stdio.h>

#define FOO3(val) do { foo(val); bar(); } while(0)

void foo(int val) {
    puts("foo");
}

void bar() {
    puts("bar");
}


int main() {
    if (2 + 2 == 4)
        FOO3(42); // { foo(42); bar(); }
    else
        foo(43);
}
