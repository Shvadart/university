#include <conio.h>
#include <locale>
#include <iostream>

extern "C" int find(char* source, int len, int*max, int*min);


void main()
{

	char *line = new char[200];
	int out;
	int max, min;
	std::cout << "Enter the line: ";
	std::cin >> line;
	out = find(line, strlen(line), &max, &min);
	if (out != 1)
	{

		printf("Maximim: ");
		printf(" %d", max-48);
		printf("\nMinimum: ");
		printf(" %d", min-48);
	}
	else
		printf("Invalid character!");
}
