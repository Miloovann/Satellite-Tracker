#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(){

char *ip = "172.27.98.68";
int port = 8888;
int n;

int server_HCIsock, client_HCIsock;
struct sockaddr_in HCI_server_addr, HCI_client_addr;
socklen_t HCI_addrsize;
char HCI_buffer2[200];

server_HCIsock = socket(AF_INET, SOCK_STREAM, 0);
if (server_HCIsock < 0){
  perror("Socket error\n");
  exit (1);
}
printf("TCP server socket created.\n");

memset(&HCI_server_addr, '\0', sizeof(HCI_server_addr));
HCI_server_addr.sin_family = AF_INET;
HCI_server_addr.sin_port = port;
HCI_server_addr.sin_addr.s_addr = inet_addr(ip);

n = bind(server_HCIsock, (struct sockaddr*)&HCI_server_addr, sizeof(HCI_server_addr));
if (n <0){
perror("Bind error");
exit(1);
}
printf("Bind to the port number: %d\n", port);

listen(server_HCIsock, 5);
printf("Listening...\n");

while(1){
HCI_addrsize = sizeof(HCI_client_addr);
client_HCIsock = accept(server_HCIsock, (struct sockaddr*)&HCI_client_addr, &HCI_addrsize);
printf("Client connected.\n");

bzero(HCI_buffer2, 200);
recv(client_HCIsock, HCI_buffer2,sizeof(HCI_buffer2), 0);
printf("Client: %s\n", HCI_buffer2);

FILE *fh = fopen("GroundPass.txt", "a");
						if(fh == NULL) {
							printf("File %s Cannot be opened.\n", "GroundPass.txt");
						} else {
							int write_sz = fwrite(HCI_buffer2, sizeof(char), 200, fh);
							if(write_sz < 200) {
								printf("Saving Failed, file size error.\n");
		    					}
						}
						printf("Complete!\n");
						fclose(fh);


bzero(HCI_buffer2, 200);
strcpy(HCI_buffer2, "Data received.");
printf("Server: %s\n", HCI_buffer2);
send(client_HCIsock, HCI_buffer2, strlen(HCI_buffer2), 0);



close(client_HCIsock);
printf("Client disconnected.\n\n");
}
return 0;

}
