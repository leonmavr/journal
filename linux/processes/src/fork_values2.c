#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

void fork_values(){
	// forked process copies the same virtual address for vars
	// BUT different physical address
	int x = 1;
	printf("Initially, x = %d at address 0x%x\n",
			x, &x);
	pid_t fork_ret = fork();
	if (fork_ret == 0)
		printf("Child has x = %d at 0x%x\n", 
				++x, &x);
	else
		printf("Parent has x = %d at 0x%x\n", 
				--x, &x);
}

int main()
{
	fork_values();
	return 0;
}
