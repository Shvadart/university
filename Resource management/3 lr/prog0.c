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

int main()
{

	setlocale (LC_TIME, "ru_RU");
	int i, n, pd[2], pid1, pid2, ppid, pid, p;	//переменные для цикла, параметр и для каналов	
	char message[500];
	int status;	
	long int gp;	
	printf("PROCESS0: Starting executing\n");
	printf("PROCESS0 create pipe\n");
	
	//Создаём канал
	p = pipe(pd);
	if (p == -1)
	{
		printf("ERROR!!!");				//Ошибка при создании канала
		return 0;
	};	
	//устанавливаем обработчики сигнала
	signal(SIGUSR1, Onsignal0);
	signal(SIGCHLD, OnSignal_died);
	
	pid = fork();//создаем процесс 1
	
	switch(pid)
	{
		case -1:
		{	
			printf("error! process1 not create\n");
			return 0;
		}		
		case 0:
		{
			char fd0[9];
			char fd1[9];
			sprintf(fd0, "%d", pd[0]);
			sprintf(fd1, "%d", pd[1]);
			execl("prog1", "prog1", fd0, fd1, NULL);
		}
	default:
		{
			//родительский процесс
			pid1 = pid;			
			printf("process0 read mes\n");
			
			for(i=0;i<3;i++)
			{
			// Читаем из канала информацию подготовленную потомками
				read(pd[0],&gp,sizeof(gp));
				read(pd[0], &message, sizeof(message));
				// Получаем номер процесса записавшего эти данные в канал   
				pid = gp;				
				printf("process0 get: %d\t%s",pid, message);
			}
		}
    }

    //ожидать завершения работы потомка
    wait();
    printf("PROCESS0: Exit\n");
}

