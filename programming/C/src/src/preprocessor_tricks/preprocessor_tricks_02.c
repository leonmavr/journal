#include <stdio.h>

#define FOO1(val) foo(val); bar();

void foo(int val) {
    puts("foo");
}

void bar() {
    puts("bar");
}


int main() {
    if (2 + 2 == 5)
        FOO1(42); // foo(42); bar()
}
