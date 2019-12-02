#include <stdio.h>

static unsigned int foo(void) 
{
	return 0xaa;
}

static inline unsigned int foo(void) __attribute__ ((always_inline));

int main(int argc, char *argv[])
{
	int i = foo();
	printf("ret = 0x%x\n", i);
	return 0;
}
