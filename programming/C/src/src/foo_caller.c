#include <stdio.h>
#include "foo_caller.h" 
#include "foo.h"

extern inline unsigned int foo(void);

void foo_caller(void)
{
	printf("foo_caller called foo at 0x%x, ret = 0x%x\n", &foo, foo());
}
