#include <stdio.h>
#include <limits.h> // USHRT_MAX

int main(int argc, char *argv[])
{
	short int shi;
	unsigned int ui;
	signed int si;
	signed char sc;
	unsigned char uc;
	signed short ss;

	// Example 1
	si = -5;
	ui = 2;
	(si + ui <= 0) ? puts("[Ex1]: -5 + 2 <= 0") :
		puts("[Ex1]: -5 + 2 > 0");

	// Example 2
	shi = -5;
	uc = 2;
	(shi + uc < 0) ? puts("[Ex2]: -5 + 2 < 0") :
		puts("[Ex2]: -5 + 2 >= 0");

	// Example 3 (http://www.idryman.org/blog/2012/11/21/integer-promotion/)
	uc = 0xff;
	sc = 0xff;
	(sc == uc) ? puts("[Ex3]: equal"):
		printf("[Ex3]: signed = 0x%x, unsigned = 0x%x\n", sc, uc);

	// Example 4
	ss = -1;
	ui = UINT_MAX;	
	printf("[Ex4]: signed = 0x%x, unsigned = 0x%x\n", ss, ui);

	// Example 5 (https://pleasestopnamingvulnerabilities.com/integers.html)
	shi = -1;
	si = 1;
	(si > shi) ? puts("[Ex5]: 1 > -1") : puts("[Ex5]: 1 <= -1");

	// Example 6
	uc = 200;
	int i = uc + 100 > uc;
	printf("[Ex 6]: %d\n", i);

	// Example 7
	uc = 200;
	i = uc + (unsigned int)100 > uc;
	printf("[Ex 6]: %d\n", i);

	// Example 8 - unsigned overflow -> wraparound
	uc = -1;
	printf("unsigned char = %u\n", uc);
}
