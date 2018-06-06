#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdio.h>
#define BUFF_SIZE 1024
//argv[1] = adresse IP d'un serveur (quelque soit le type de service(ssh, telnet, smtp..))
// par ex : "129.194.187.176" (168)
//argv[2] = le numéro de port sur lequel tourne le service (par ex:80 pour http)
/* AF_INET= ipv4, SOCK_STREAM corresponds à TCP*/

int main(int argc, char *argv[])
{
    int s;
    struct sockaddr_in addr_internet;

    if(argc<2) {
        printf("Usage : %s <addr_ip> <port>\n", argv[0]);
        exit(1);
    }


    if((s=socket(AF_INET, SOCK_STREAM,0))<0) {
        perror("socket");
        exit(1);
    }

    addr_internet.sin_family=AF_INET;
    addr_internet.sin_port = (in_port_t)htons(atoi(argv[2]));
    addr_internet.sin_addr.s_addr = inet_addr(argv[1]);

    if((connect(s, (struct sockaddr *)&addr_internet, sizeof(addr_internet))<0))
        perror("connect");


    /* initialisation terminée */

    ssize_t nread;
    char buff_e[BUFF_SIZE];
    char buff_r[BUFF_SIZE];
    while(1) { 
        nread=read(0,buff_e,BUFF_SIZE);
        write(s,buff_e,nread);
        //nread=read(s,buff_r,BUFF_SIZE);
        //write(1,buff_r,nread);
        
    }

    close(s);
	
	return EXIT_SUCCESS;

}
