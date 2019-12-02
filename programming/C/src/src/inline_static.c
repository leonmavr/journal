#include <stdio.h>

static inline unsigned int square(int x)
{
	return x*x;
}

int main(int argc, char *argv[])
{
	unsigned int i = square(5);	
	printf("address = 0x%x, return = 0x%x\n", (unsigned int) &square, i);
	return 0;
}
