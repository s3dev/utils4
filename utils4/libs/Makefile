CFLAGS=-Wall -pedantic -std=gnu99 -Wsign-compare -Wwrite-strings -Wtype-limits

test: test.c libmfunc.c
	gcc ${CFLAGS} -o test test.c libmfunc.c -lm

.PHONY: clean
clean:
	@printf "Cleaning source directory ...\n"
	@rm *.o *.so
	@printf "Done.\n"

