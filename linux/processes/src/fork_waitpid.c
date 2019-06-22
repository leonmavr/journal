#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main() 
{
  int status;
  printf("%s\n", "Hello");
  printf("%d\n", !fork());
  // waitpid(-1, ... -> wait for any child process
  if(waitpid(-1, &status, 0) != -1) {
    printf("%d\n", WEXITSTATUS(status));
  }
  printf("%s\n", "Bye");
  exit(2);
}
