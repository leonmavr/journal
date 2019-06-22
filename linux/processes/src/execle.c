#include <unistd.h>
#include <stdio.h>

int main() {
	/* Executes env given some arguments in  envp */
	char* fpath = "/bin/sh";
    char* arg[] = { fpath, "-c", "env", NULL };
    char* envp[] =
    {
        "HOME=/",
        "PATH=/bin:/usr/bin",
		"USER=leo", 
		"TERM=xterm", 
		NULL
    };
    execle(fpath, arg[0], arg[1], arg[2], NULL, envp);
    fprintf(stderr, "Oops!\n");
    return -1;
}
