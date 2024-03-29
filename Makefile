CC      = cc
CFLAGS  = -std=gnu11 -Wall -Wextra -Werror -g
LDLIBS  = -lnsl -lpthread -lrt

PROG    = count
OBJS    = count.o csapp.o

all: ${PROG}

${PROG}: ${OBJS}
	${CC} ${CFLAGS} -o ${PROG} ${OBJS} ${LDLIBS}

csapp.o: ${COURSE}/src/csapp.c ${COURSE}/include/csapp.h
	${CC} ${CFLAGS} -I${COURSE}/include -c $< 

count.o: count.c ${COURSE}/include/csapp.h
	${CC} ${CFLAGS} -I${COURSE}/include -c $< 

clean:
	${RM} *.o ${PROG} core.[1-9]*

.PHONY: clean