#include <stdio.h>
#include "sstr.h" 

unsigned int sstrlen(const char* pSrc)
{
	const char* start = pSrc;
	while (*++pSrc);
	return pSrc - start; 
}


void sstrCpy(const char* pSrc, char* pDst)
{
	while (*pDst++ = *pSrc++);
}


void sstrrev(const char* pSrc, char* pDst)
{
	pSrc += sstrlen(pSrc) - 1;
	while (*pDst++ = *pSrc--);
}


char sstrLower(const char c)
{
	return c + 32; // ASCII table
}


unsigned int sstrPalin(const char* pSrc)
{
	int len = sstrlen(pSrc);
	// empty string or one letter
	if (len == 1 || len == 0) 
		return 1;
	const char *start = pSrc;
	const char *end = pSrc + len - 1;
	while (end-- >= start++)
		if (*end != *start)
			return 0;
	return 1;
}


void sstrPrint(char* pSrc)
{
	while (*pSrc)
	{
		printf("%c", *pSrc);
		pSrc++;
	}
	printf("\n");
}
