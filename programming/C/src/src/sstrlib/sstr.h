#ifndef SSTR_H
#define SSTR_H 

unsigned int sstrlen(const char* pSrc);

void sstrCpy(const char* pSrc, char* pDst);

void sstrrev(const char* pSrc, char* pDst);

char sstrLower(const char c);

unsigned int sstrPalin(const char* pSrc);

void sstrPrint(char* pSrc);
#endif /* SSTR_H */
