#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MAX_SIZE	1024

int main(){

        char *ip = "172.27.98.68";//may need to change, check it before running this code
        int port = 8888;
        int n;

        int server_HCIsockTest, client_HCIsockTest;
        struct sockaddr_in HCI_serverTest_addr, HCI_clientTest_addr;
        socklen_t HCI_addrsizeTest;
        char HCI_buffer[MAX_SIZE];

        server_HCIsockTest = socket(AF_INET, SOCK_STREAM, 0);
        if (server_HCIsockTest < 0)
        {
                perror("Socket error\n");
                exit (1);
        }
        printf("TCP server socket created.\n");

        memset(&HCI_serverTest_addr, '\0', sizeof(HCI_serverTest_addr));
        HCI_serverTest_addr.sin_family = AF_INET;
        HCI_serverTest_addr.sin_port = port;
        HCI_serverTest_addr.sin_addr.s_addr = inet_addr(ip);

        n = bind(server_HCIsockTest, (struct sockaddr*)&HCI_serverTest_addr, sizeof(HCI_serverTest_addr));
        if (n <0)
        {
                perror("Bind error");
                exit(1);
        }
        printf("Bind to the port number: %d\n", port);

        listen(server_HCIsockTest, 5);
        printf("Listening...\n");

        while(1){
                HCI_addrsizeTest = sizeof(HCI_clientTest_addr);
                client_HCIsockTest = accept(server_HCIsockTest, (struct sockaddr*)&HCI_clientTest_addr, &HCI_addrsizeTest);
                printf("Client connected.\n");

                bzero(HCI_buffer, MAX_SIZE);
                int BUF_SIZE;
                BUF_SIZE = recv(client_HCIsockTest, HCI_buffer,sizeof(HCI_buffer), 0);
                printf("Client: %s\n", HCI_buffer);
                printf("%d\n", BUF_SIZE);

                if (BUF_SIZE < 200)
                {
                        FILE *fh = fopen("projected.txt", "a");
			        if(fh == NULL) {
				        printf("File %s Cannot be opened.\n", "projected.txt");
				} else {
				        int write_sz = fwrite(HCI_buffer, sizeof(char), BUF_SIZE, fh);
				        if(write_sz > MAX_SIZE) {
                                                printf("Saving Failed, file size error.\n");
		    			        }
					}
					printf("Complete!\n");
					fclose(fh);
                } else {
                        FILE *fh = fopen("AOSLOS.txt", "w");
				if(fh == NULL) {
					printf("File %s Cannot be opened.\n", "AOSLOS.txt");
				} else {
					int write_sz = fwrite(HCI_buffer, sizeof(char), BUF_SIZE, fh);
					if(write_sz > MAX_SIZE) {
						printf("Saving Failed, file size error.\n");
		    				}
					}
					printf("Complete!\n");
					fclose(fh);
                }


                bzero(HCI_buffer, MAX_SIZE);
                strcpy(HCI_buffer, "Hi, server have received the message.");
                printf("Server: %s\n", HCI_buffer);
                send(client_HCIsockTest, HCI_buffer, strlen(HCI_buffer), 0);

                close(client_HCIsockTest);
                printf("Client disconnected.\n\n");
        }

return 0;

}
