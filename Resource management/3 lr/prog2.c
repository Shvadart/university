#include<unistd.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<sys/dir.h>      
#include<fcntl.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<signal.h>
#include <locale.h>

void Onsignal0()
{
	printf("I'm process0. I get signal.\n");
}
void Onsignal1()
{
	printf("I'm process1. I get signal.\n");
}
void Onsignal2()
{
	printf("I'm process2. I get signal.\n");
}
void OnSignal_died()
{
	printf("I'm in OnSiganl_died\n");	
}

int main(int argc, char *argv[])
{
    int i, n, pd[2], pid1, pid2, ppid, pid, p;	//переменные для цикла, параметр и для каналов	
	char message[500];
	int status;	
	long int gp;
    int fd0 = atoi(argv[1]);
	int fd1 = atoi(argv[2]);
	pd[0] = fd0;
	pd[1] = fd1;  
    printf("process2 create\n");
					printf("process2 wait signal from process1\n");
					//устанавливаем обработчики сигнала
					signal(SIGUSR1, Onsignal2);
					signal(SIGCHLD, OnSignal_died);
					
					pause();//ждем сигнала
					
					gp = getpid();//получаем идентификатор процесса
					strcpy(message, "          I'm proccess2. I'm busy\n");					
					printf("process2 sent mes in chanel\n");
					
					//записываем в канал информацию от второго процесса
					write(pd[1], gp, sizeof(gp));
					write(pd[1], message, sizeof(message));
					
					ppid = getppid();//получаем предка второго процесса
					printf("process2 sent mes for process1\n");
					kill(ppid, SIGUSR1);//отправляем сигнал процессу 1
					printf("process2 finished \n");
					exit(0);
}
