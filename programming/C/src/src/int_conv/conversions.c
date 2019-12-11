#include <stdio.h>
#include <limits.h>

#ifndef EXAMPLE
#define EXAMPLE 5
#endif

int main(int argc, char *argv[])
{
#if EXAMPLE == 0
	signed char sc = -1;
	unsigned short ush = 0;
	(sc + ush < ush)? puts("[1]: -1 < 0"): puts("[1]: -1 >= 0")
#elif EXAMPLE == 1
	signed short ssh = -1;
	int si = 0;
	(ssh + si < si)? puts("[2]: -1 < 0"): puts("[2]: -1 >= 0");
#elif EXAMPLE == 2
	signed short ssh = -1;
	int si = 0;
	(ssh + si < 0U)? puts("[3]: -1 < 0"): puts("[3]: -1 >= 0");
#elif EXAMPLE == 3
	int si = -1;
	unsigned long ul = 0;
	(si + ul < ul)? puts("[4]: -1 < 0"): puts("[4]: -1 >= 0");
#elif EXAMPLE == 4
	char sc = -2;
	signed char uc = 1;
	(sc + uc == -1)? puts("[5]: -1"): puts("[5] != -1");
#elif EXAMPLE == 5
	signed int si = -5;
	unsigned int ui = 2;
	(si + ui == -3)? puts("[6]: -5+2==-3"): puts("[6]: -5+2!=-3");
#endif
	return 0;
}
