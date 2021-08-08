#include <stdio.h>

int main(int argc, char *argv[])
{
    int arr[2] = {0, 1};
    const int* ptrToConst = arr; // a.k.a. &arr[0]
    ptrToConst++; // <- OK
    arr[1]++; // <- OK
    //++*ptrToConst; // <- not OK - read-only variable is not assignable
    //*ptrToConst = 2; // <- not OK - read-only variable is not assignable
    printf("\n%d\n", *ptrToConst);
    return 0;
}
