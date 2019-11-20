#include <stdio.h>
#include "foo.h" 

inline unsigned int foo(void);

int main(int argc, char *argv[])
{
	printf("address = 0x%x, ret = 0x%x\n", &foo, foo());
	return 0;
}
