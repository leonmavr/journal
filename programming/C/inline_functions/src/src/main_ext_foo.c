#include <stdio.h>
#include "foo_caller.h"

extern inline unsigned int foo(void);

int main(int argc, char *argv[])
{
	foo_caller();	
	printf("foo called from main at 0x%x, ret = 0x%x\n", &foo, foo());
	return 0;
}
