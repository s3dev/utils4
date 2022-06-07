CFLAGS=-Wall -pedantic -std=gnu99 -Wsign-compare -Wwrite-strings -Wtype-limits

test: test.c _mathfunc.c
	gcc ${CFLAGS} -o test test.c _mathfunc.c -lm

.PHONY: clean
clean:
	@printf "Cleaning source directory ...\n"
	@rm *.o *.so
	@printf "Done.\n"

