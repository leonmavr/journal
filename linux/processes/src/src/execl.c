#include <unistd.h>    // exec*

int main () {
	/* Executes ls -l / */
	char* cmd = "/bin/ls";// executable
	char* argv0 = "ls";   // name to use
	char* argv1 = "-l";   // cmd arg
	char* argv2 = "/";    // cmd arg
	char* argv3 = NULL;   // terminator

	return execl (cmd, argv0,  argv1,
	argv2, NULL);
}
