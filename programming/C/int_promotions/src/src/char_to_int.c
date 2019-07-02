#include <stdio.h>

char foo(char c1, char c2, char c3) {
	char res = c1 * c2 / c3;
	printf("%d, %d, %d\n", 
			res, sizeof(res), sizeof(c1*c2/c3));
	return res; 
}

int main()
{
	// ASCII '(' = decimal 40
	foo(100, 4, '(');
}
