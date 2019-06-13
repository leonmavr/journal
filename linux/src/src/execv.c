#include <unistd.h>    // exec*

int main () {
	/* Executes ls -l / */
	char* cmd = "/bin/ls";
	char* argv[4];
	argv[0] = "ls";
	argv[1] = "-l";
	argv[2] = "/";
	argv[3] = NULL;

	return execv(cmd,  argv);
}
