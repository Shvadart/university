#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <time.h>
#define K 5	//кол-во записей в таблице и кол-во потомков

struct table	 //таблица
{
    char msg[20];
} ;

struct message 	// структура сообщения
	{
	 long mtype;            	/* тип сообщения */
	 char mtext[20]; 	/* текст сообщения (SOMEVALUE - любое) */
	};

void read(struct table tab[K], FILE *f)//ввод таблицы
{
	int i;
	char s[20];

	for (i=0; i<K; i++)
	{
		fscanf(f, "%s", &s);
		strcpy(tab[i].msg, s);;
	}
}

void add_queue(int i, int done)		//добавление сообщение в очередь сообщений
{
    	struct message msg;

	if (done < 0)
        	printf("ERROR KEY");
	else
		{   
			//формируем сообщение
sprintf(msg.mtext,"%d %d",getpid(),i);//добавляем в сообщение идентификатор потомка и номер строки
			msg.mtype=1;//тип = 1
			//добавляем в очередь
			msgsnd(done,(void*)&msg,20,0);
        		}
}

char* delete_tab(struct table tab[5], int msgid_in) //удаление строк из таблицы
{

	struct message msg;
	char* res;
	int i;

	int row,pid;

	//ждем по 1му сообщению от каждого потомка
	
		//получаем сообщени
	
		msgrcv(msgid_in,&msg,20,1,0);

		//считываем номер строки
        sscanf(msg.mtext,"%d %d",&pid,&row);

		//удаляем
		strcpy(res, tab[row].msg);
		printf("proc %d  %s", pid, res);
        tab[row].msg[0] = '\0';
	return res;
}

int main()
{
    struct table tab[K];
	int i , j, pid_pr;
	char* res;
	int pids[K];
	int msg_in;

	key_t qkey_in= IPC_PRIVATE; //ключ для очереди


   	 //открываем файл с данными для таблицы
	FILE *f_in = fopen("data.txt", "r");
	read(tab,f_in);
	//создаем очередь
    	msg_in = msgget(qkey_in, 0666 | IPC_CREAT);

 if( msg_in < 0 )
{
		printf("ERROR : queue don't create\n");
		return 1;
}
	//создаем потомков
	for(i=0; i<K; i++)
	{
		switch(pid_pr = fork())
		{
			case -1:
			{
				printf("ERROR");
				for(j=0; j<i; j++)
				kill(j, SIGKILL);
			}
			case 0:
			{
                add_queue(i,msg_in);
               	return 0;
			}

        }
	}

for(i=1; i<K+1; i++ )
{
	res = delete_tab(tab, msg_in);
	printf("delete %s\n", res);
}
msgctl(msg_in,IPC_RMID,NULL);
return 0;
}

