#include <stdio.h>
#include "foo.h"

extern inline unsigned int foo(void);

int main(int argc, char *argv[])
{	
	unsigned int i = foo();
	printf("address of foo = 0x%x, ret = 0x%x\n", &foo, i);
	return 0;
}
