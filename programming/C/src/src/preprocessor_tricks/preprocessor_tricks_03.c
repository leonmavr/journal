#include <stdio.h>

#define FOO2(val) { foo(val); bar(); }

void foo(int val) {
    puts("foo");
}

void bar() {
    puts("bar");
}


int main() {
    if (2 + 2 == 4)
        FOO2(42);
}
