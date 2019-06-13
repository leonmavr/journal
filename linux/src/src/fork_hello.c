#include <stdio.h> 
#include <sys/types.h> 
#include <unistd.h> 

int main() { 
    printf("Hello world!\n"); 
    // make two process which run same 
    // program after this instruction 
    fork(); 
  
    printf("Bye world!\n"); 
    return 0; 
} 
