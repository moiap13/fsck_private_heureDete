CC=gcc
FLAGS=-Wall -Wextra -std=gnu11
OBJS= client server 

client: client.c
	$(CC) $(FLAGS) $^ -o client 

server: server.c
	$(CC) $(FLAGS) $^ -o server -lm

clean:
	rm -rf *.o $(OBJS)

all: client server

c: client
	./client 129.194.187.128 1242

s: server
	./server 1242