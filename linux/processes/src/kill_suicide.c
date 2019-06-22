#include <stdio.h> 
#include <signal.h> 
#include <unistd.h>
#include <sys/types.h> // pid_t
#include <time.h>

void suicide(){
	pid_t myPid = getpid();
	printf("My PID is %d\n", myPid);
	/* Look it up on a terminal */
	sleep(30);
	kill(myPid, SIGINT);
	/* Look up again */
}

int main()
{
	suicide();
	return 0;
}
