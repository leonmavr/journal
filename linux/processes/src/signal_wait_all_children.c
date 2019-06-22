/*
 * adapted from: http://www.cs.cmu.edu/afs/cs/academic/class/15213-f05/code/ecf/forks.c
 */
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#define N 5
int ccount = N;

/*
 * child_handler2 - SIGCHLD handler that reaps all terminated children
 */
void child_handler2(int sig)
{
	int child_status;
	pid_t pid;
	/* reap the zombie processes */
	while ((pid = wait(&child_status)) > 0) {
		ccount--;
		/* NOT recommended to use printf here - for debug only */
		printf("Received signal %d from process %d\n", sig, pid);
	}
}

/*
 * fork15 - Using a handler that reaps multiple children
 */
void fork15()
{
	pid_t pid[N];
	int i;

	/* call child_handler2 when SIGCHLD is received */
	signal(SIGCHLD, child_handler2);

	for (i = 0; i < N; i++)
		if ((pid[i] = fork()) == 0) {
			printf("Created child with PID %d\n", getpid());
			/* Child: Exit (and emit SIGCHLD) */
			exit(0);
		}
	/* 
	 * pause() - waits for any signal. 
	 * Without this parent may exit before waiting.
	 */
	while (ccount > 0) {
		pause();
	}
}

int main()
{
	fork15();
	return 0;
}
