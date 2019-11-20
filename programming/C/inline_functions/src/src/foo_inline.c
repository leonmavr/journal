#include <stdio.h>
#include "foo_inline.h" 

int main(int argc, char *argv[])
{	
	unsigned int i = foo();
	printf("address of foo = 0x%x, ret = 0x%x\n", &foo, i);
	return 0;
}
