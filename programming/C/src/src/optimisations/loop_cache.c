#include <stdio.h>
#include <unistd.h> // sleep()


int foo() {
	sleep(1);
	return 1337;
}


int main(int argc, char *argv[])
{
	// Don't do this
	//for (int i = 0; i < foo(); ++i)	
	// Do this instead
	for (int len = foo(), i = 0; i < len; ++i)	
		puts(".");
	return 0;
}
