#include <stdio.h>

static inline int foo(int x) {
	return x*x;
}

int main(int argc, char *argv[])
{
	int i = foo(4);
	printf("%d/n", i);
	return 0;
}
