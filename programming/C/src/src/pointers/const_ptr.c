#include <stdio.h>

int main(int argc, char *argv[])
{
    int i = 0, j = 1;
    int* const constPtr = &i;
    *constPtr = 2; // <- OK
    ++*constPtr; // <- OK
    printf("\n%d\n", *constPtr);
    //constPtr = &j;  // <- not OK
    return 0;
}
