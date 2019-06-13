#include <stdio.h> 
#include <sys/types.h> 
#include <unistd.h> 

int main() { 
	// Each fork runs recusrively the rest of the program
    fork(); 
    fork(); 
    fork(); 
  
    printf("Hello world!\n"); 
    return 0; 
} 
