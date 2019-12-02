#ifndef TRY_TO_INLINE_ME_H
#define TRY_TO_INLINE_ME_H 

#include <time.h>
#include <stdlib.h>

unsigned int try_to_inline_me(void)
{
	srand(time(NULL));
	int i, r;
	int ret = 0;
	for (i = 0; i < 9999; ++i) {
		r = rand() % 1337;
		ret += r;
	}
	return ret;
}

#endif /* TRY_TO_INLINE_ME_H */
