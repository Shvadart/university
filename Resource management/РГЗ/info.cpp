#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#include <stdio.h>
#include <tchar.h>
#include <windows.h>

void mycpuid(int regs[4], int func)
{
	int ieax, iebx, iecx, iedx;
	_asm
	{
		mov eax, func
		cpuid
		mov ieax, eax
		mov iebx, ebx
		mov iecx, ecx
		mov iedx, edx
	}
	regs[0] = ieax;
	regs[1] = iebx;
	regs[2] = iecx;
	regs[3] = iedx;
}

/// <summary> 
/// Вызов команды cpuid со входным значением EAX = 4. 
/// Возвращаемое значение - размер кэша данных первого уровня.
/// </summary>
int leaf4()
{
	int ieax, iebx, iecx;
	int icache = 0, func = 0x04;
	do
	{
		_asm
		{
			mov eax, func
			mov ecx, icache
			cpuid
			mov ieax, eax
			mov iebx, ebx
			mov iecx, ecx
		}

		/* Если возвращена информация о кэше данных первого уровня:
		EAX[7:5] = 001, EAX[4:0] = 00001 */
		if ((ieax & 0xFF) == 0x21)
		{
			unsigned int ways = (iebx >> 22) & 0x3FF;		// EBX[31:22]
			unsigned int partitions = (iebx >> 12) & 0x3FF;	// EBX[21:12]
			unsigned int linesize = iebx & 0xFFF;			// EBX[11:0]
			unsigned int sets = iecx;						// ECX[31:0]

			unsigned int L1Size = (ways + 1)*(partitions + 1)*(linesize + 1)*(sets + 1) >> 10;

			return L1Size;
		}

		icache++;

	} while ((ieax & 0xF) != 0);
}

extern "C" _declspec(dllexport) int Information(char *InfoString)
{
	/* Узнать имя компьютера */
	DWORD computerNameLen;
	sscanf(InfoString, "%i", &computerNameLen);
	TCHAR *computerName = new TCHAR[computerNameLen];
	GetComputerName((LPWSTR)computerName, &computerNameLen);
	sprintf(InfoString, "%i", computerNameLen);
	wsprintf((LPWSTR)(InfoString + 4), (LPWSTR)computerName);

	/* Узнать размер кэша данных первого уровня */
	/* Определить производителя */
	unsigned int L1Size;
	int CPUInfo[4];
	char VendorID[13];
	VendorID[12] = '\0';
	mycpuid(CPUInfo, 0x0);
	memcpy(VendorID, CPUInfo + 1, sizeof(int));
	memcpy(VendorID + 4, CPUInfo + 3, sizeof(int));
	memcpy(VendorID + 8, CPUInfo + 2, sizeof(int));

	/* Процессор компании Intel */
	if (strcmp(VendorID, "GenuineIntel") == 0)
	{
		/* Дескрипторы и соответствующие им значения размера кэша данных первого уровня */
		short desc[9] = { 0x0A, 0x0C, 0x0D, 0x0E, 0x2C, 0x60, 0x66, 0x67, 0x68 };
		short size[9] = { 8, 16, 16, 24, 32, 16, 8, 16, 32 };

		int rep = 0, n;
		do
		{
			mycpuid(CPUInfo, 0x02);
			rep++;

			/* Содержимое регистра AL: сколько раз нужно
			выполнить команду cpuid со входным значением 0x02,
			чтобы получить достоверную информацию о микропроцессоре */
			n = CPUInfo[0] & 0xFF;

		} while (rep < n);

		/* Младший байт EAX игнорируется */
		CPUInfo[0] &= ~0xFF;

		/* Цикл по регистрам */
		for (int i = 0; i < 4; i++)
		{
			/* Если старший бит равен 0, регистр
			содержит достоверную информацию */
			if ((CPUInfo[i] & 0x80000000) == 0)
			{
				/* Цикл по байтам */
				for (int j = 0; j < 4; j++)
				{
					short byte = (CPUInfo[i] >> j * 8) & 0xFF;
					for (int k = 0; k < 9; k++)
						if (byte == desc[k])
						{
							L1Size = size[k];
							wsprintf((LPWSTR)(InfoString + 4) + computerNameLen, L"%i", L1Size);
							return 1;
						}
						else if (byte == 0xFF)
						{
							/* Байт 0xFF указывает на то, что информацию
							о кэше нужно получать с помощью команды cpuid
							со входным значением 0x04 (относится к
							специфическим функциям модели) */

							L1Size = leaf4();
							wsprintf((LPWSTR)(InfoString + 4) + computerNameLen, L"%i", L1Size);
							return 1;
						}
				}
			}
		}
	}
	/* Процессор компании AMD */
	else if (strcmp(VendorID, "AuthenticAMD") == 0)
	{
		mycpuid(CPUInfo, 0x80000005);
		L1Size = (CPUInfo[2] >> 24) & 0xFF; // ECX[31:24]
		wsprintf((LPWSTR)(InfoString + 4) + computerNameLen, L"%i", L1Size);
		return 1;
	}

	return 0;
}