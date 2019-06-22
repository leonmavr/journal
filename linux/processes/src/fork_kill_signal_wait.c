#include <stdio.h> 
#include <signal.h> 
#include <wait.h> 
#include <stdlib.h> // exit, NULL
#include <unistd.h> // fork

#define N 3
/*
int_handler - SIGINT handler
 */
void int_handler(int sig)
{
	printf("Process %d received signal %d\n", getpid(), sig);
	exit(0);
}

/*
 * fork13 - Simple signal handler example
 */
void fork13()
{
	pid_t pid[N];
	int i;
	int child_status;

	signal(SIGINT, int_handler);
	for (i = 0; i < N; i++)
		if ((pid[i] = fork()) == 0) {
			/* Child: Infinite Loop */
			while(1)
				;
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

int main()
{	
	fork13();
	return 0;
}



