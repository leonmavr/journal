#define _POSIX_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h> 
#include <signal.h>

#define N 5

/*
 * int_handler - SIGINT handler
 */

void fork12()
{
	pid_t pid[N];
	int i;
	int child_status;

	for (i = 0; i < N; i++){
		if ((pid[i] = fork()) == 0) {
			/* Child: Infinite Loop */
			while(1)
				;
		}
	}
	for (i = 0; i < N; i++) {
		printf("Killing process %d\n", pid[i]);
		kill(pid[i], SIGINT);
	}

	for (i = 0; i < N; i++) {
		pid_t wpid = wait(&child_status);
		if (WIFEXITED(child_status))
			printf("Child %d terminated with exit status %d\n",
					wpid, WEXITSTATUS(child_status));
		else
			printf("Child %d terminated abnormally\n", wpid);
	}
}


int main(int argc, char *argv[])
{
	fork12();
	return 0;
}
