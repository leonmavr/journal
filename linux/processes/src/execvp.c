#include <unistd.h>    // exec*

int main () {
	/* Executes ls -l / */
	char* cmd = "ls";
	char* argv[4];
	argv[0] = "ls";
	argv[1] = "-l";
	argv[2] = "/";
	argv[3] = NULL;

	return execvp (cmd,  argv);
}
