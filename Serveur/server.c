#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <fcntl.h>
#include <errno.h>
#include <math.h>

/* argv[1] = le numéro de port sur lequel tourne le service (par ex:80 pour http) */
/* AF_INET= ipv4, SOCK_STREAM corresponds à TCP*/
#define BUFF_SIZE 1024
#define PATH_FILE "img/minixfs_lab1.img"
#define MAGIC_REQ 0x76767676
#define MAGIC_ANS 0x87878787
#define CMD_READ 0x0
#define MAGIC_STOP 0x21212121 

typedef struct {
	int magic;
	int type;
	int handle;
	int offset;
	int length;
} request_t;

typedef struct {
	int magic;
	int error;
	int handle;
	unsigned int *payload;
} answer_t;

int get_data(int start, int length, unsigned int output[]){
	int descr;
	if((descr = open(PATH_FILE, O_RDONLY)) < 1) 
		return -1;
		
	if(lseek(descr, start, SEEK_SET) == (off_t) -1)
		return -1;
		
	if(read(descr,output,length) < 0)
		return -1;
	printf("%d\n",(short) output[0]);
	return 0; //reussi
}
void test_img(){
/*
	unsigned short buff[1024];
	int n = get_data(1024*6,1024,buff); 
	
	printf("%d\n", buff[0]);
	printf("%d\n", buff[1020]);
	printf("%d\n", buff[1021]);*/
}
int main(int argc, char *argv[])
{
    int s;
    struct sockaddr_in addr_internet;
    struct sockaddr_in addr_client;
    
    if(argc<2) {
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }


    if((s=socket(AF_INET, SOCK_STREAM,0))<0) {
        perror("socket");
        exit(1);
    }

    addr_internet.sin_family=AF_INET;
    addr_internet.sin_port = (in_port_t)htons(atoi(argv[1]));
    addr_internet.sin_addr.s_addr = htonl(INADDR_ANY);

    if((bind(s, (struct sockaddr *)&addr_internet, sizeof(addr_internet)))<0)
        perror("bind");

    if(listen(s, 10)<0)
        perror("listen");

    socklen_t len_client;
    int new_socket;
    while(1){
		 if((new_socket=accept(s, (struct sockaddr *)&addr_client, &len_client))<0)
		     perror("accept");
		     
		int pid = fork();	
		
		if(pid == 0){
		//enfant
			break;
		}
		else if(pid < 0){
			perror("fork");
		}
		
    }

    printf("New client\n");
	 int buff_e[6] = {0};
    char buff_r[BUFF_SIZE];
    /* initialisation terminée */
	
	 /* code enfant */
    ssize_t nread;
   buff_e[6] = 0;
   
   while(1){
   	memset(buff_e, 0, BUFF_SIZE);
		 nread=read(new_socket,buff_e,BUFF_SIZE);
	 
		 request_t *req = (request_t *) buff_e;
		 printf("magic=%d\n",req->magic);
		 if(req->magic == MAGIC_REQ ){ // VERIFIER LE CMD READ
		 	
			 unsigned int output[req->length];
			 int err = get_data(req->offset, req->length, output);
			 answer_t ans;
			 printf("s%d\n", sizeof(ans));
			 ans.payload = malloc(req->length);
			 memset(ans.payload, 0, req->length);
			 strcpy(ans.payload, output);
			 ans.magic = MAGIC_ANS;
			 ans.error =err;
			 ans.handle = req->handle;
			 printf("s%d\n", sizeof(ans));
			 int l = 3+ (int) ceil(req->length/4);
			 int salut[l];
			 salut[0] = MAGIC_ANS;
			 salut[1] = err;
			 salut[2] = req->handle;
			 //copie du payload
			 for(int i = 3; i < l; i++){
			 	salut[i] = output[i-3];
			 }		 	
			 write(new_socket, salut, sizeof(salut));
		 } else if(req->magic ==  MAGIC_STOP){
		 		write(new_socket, "salut\n", 6);
			 	printf("fin de connexion\n");
			 	close(s);
			 	break;
		 }
		 else{
		 	write(1,buff_e,BUFF_SIZE);
		 	write(1,"\n",1);
		 	exit(0);
		 }
    }

    
    return 0;
}
