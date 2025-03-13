
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
	int fd0 = atoi(argv[1]);
	int fd1 = atoi(argv[2]);
	pd[0] = fd0;
	pd[1] = fd1;
	int status;	
	long int gp;
    printf("process1 create\n");
	printf("process1 fork process2\n");
			pid = fork(); // процесс 2
			//устанавливаем обработчики сигнала
			signal(SIGUSR1, Onsignal1);
			signal(SIGCHLD, OnSignal_died);
			
			switch(pid)
			{
				case -1:
				{
					printf("error! process2 not create\n");
					return 0;
				}
				
				case 0:
				{
					char fd0[9];
					char fd1[9];
					sprintf(fd0, "%d", pd[0]);
					sprintf(fd1, "%d", pd[1]);
					execl("prog2", "prog2", fd0, fd1, NULL);
				}
				default:
				{
					//процесс потомка
					pid2 = pid;
					gp = getpid();	//получаем идентификатор
					
					printf("process1 sent mes in chanel\n");	
					strcpy(message, "          I'm proccess1. I'm busy\n");	
					//записываем в канал информацию от первого процесса
					write(pd[1], gp, sizeof(gp));				
					write(pd[1], message, sizeof(message));
										
					printf("process1 sent signal for process 2\n");
					kill(pid2, SIGUSR1);//отправляем сигнал второму
					//потомок P1 приостанавливает свое выполнение до поучения сигнала SIGUSR1
					printf("process1 wait signal from procces 2\n");
					pause(); //ждем сигнала
					
					printf("process1 sent mes in chanel\n");
					strcpy(message, "          I'm process1, I'm free\n");			
					//записываем в канал информацию от первого процесса
					write(pd[1],gp,sizeof(gp));
					write(pd[1], message, sizeof(message));
					
					//ожидать завершения работы потомка
					wait(&status);
					printf("process1 finished\n");
					exit(0);
				}
			}
}