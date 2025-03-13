#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#include <windows.h>
#include <tchar.h>
#include <string>

#define BUFFER_SIZE 64

LPCWSTR szClassName = L"MyClass";
LPCWSTR szTitle = L"Индивидуальное задание по УРВС";

TCHAR computerName[BUFFER_SIZE];
DWORD computerNameLen;

DWORD L1Size;
TCHAR L1Info[BUFFER_SIZE];

DWORD WINAPI ThreadFunc(void *)
{
	/* Подключение библиотеки */
	typedef int(*ImportFunction)(char *);
	ImportFunction DLLInfo;
	HINSTANCE hinstLib = LoadLibrary(TEXT("info.dll"));
	DLLInfo = (ImportFunction)GetProcAddress(hinstLib, "Information");

	char String[BUFFER_SIZE + 8];
	computerNameLen = BUFFER_SIZE - 16;
	sprintf(String, "%i", computerNameLen);

	/* Вызов функции из динамической библиотеки */
	int res = DLLInfo(String);
	/* Освобождение дескриптора */
	FreeLibrary(hinstLib);

	/* Интерпретация выходных данных функции DLLInfo */
	sscanf(String, "%i", &computerNameLen);
	wsprintf(computerName, L"Имя компьютера: %ls", (TCHAR *)(String + 4));

	if (res)
	{
		swscanf((LPWSTR)(String + 4) + computerNameLen, L"%i", &L1Size);
		wsprintf(L1Info, L"Размер кэша данных первого уровня: %i Кбайт", L1Size);
	}
	else 
		wsprintf(L1Info, L"Не удалось определить размер кэша данных первого уровня.");

	return 1;
}

LRESULT CALLBACK WindowFunc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
	PAINTSTRUCT ps;
	HDC hDC;
	HFONT hFont = CreateFont(18, 0, 0, 0, FW_THIN, TRUE, FALSE, FALSE, DEFAULT_CHARSET, OUT_OUTLINE_PRECIS,
		CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, VARIABLE_PITCH, TEXT("Times New Roman"));

	switch (msg)
	{
	case WM_CREATE:
		/* Создание потока */
		HANDLE hThread;
		DWORD IDThread;
		hThread = CreateThread(NULL, 0, ThreadFunc, NULL, 0, &IDThread);
		WaitForSingleObject(hThread, INFINITE); // Ожидание завершения потока
		CloseHandle(hThread); // Удаление дескриптора потока
		break;

	case WM_DESTROY:
		/* Закрытие окна */
		PostQuitMessage(0);
		break;

	case WM_PAINT:
		/* Инициализация контекста устройства*/
		hDC = BeginPaint(hWnd, &ps);
		SelectObject(hDC, hFont);
		SetTextColor(hDC, RGB(0, 64, 128));
		TextOut(hDC, 15, 17, computerName, (int)computerNameLen + 16);
		TextOut(hDC, 15, 42, L1Info, 50);
		EndPaint(hWnd, &ps);
		break;

	default:
		return DefWindowProc(hWnd, msg, wParam, lParam);
	}
	return 0;
}

int WINAPI WinMain(HINSTANCE hThisInst, HINSTANCE hPrevInst,
	LPSTR str, int nWinMode)
{
	MSG msg;
	WNDCLASS wcl;
	HWND hWnd;

	/* Создание класса окна */
	wcl.hInstance = hThisInst;
	wcl.lpszClassName = szClassName;
	wcl.lpfnWndProc = WindowFunc;
	wcl.style = CS_HREDRAW | CS_VREDRAW;
	wcl.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wcl.hCursor = LoadCursor(NULL, IDC_ARROW);
	wcl.lpszMenuName = NULL;
	wcl.cbClsExtra = 0;
	wcl.cbWndExtra = 0;
	wcl.hbrBackground = (HBRUSH)GetStockObject(DEFAULT_PALETTE);
	/* Регистрация класса окна */
	RegisterClass(&wcl);
	/* Создание окна на базе созданного класса */
	hWnd = CreateWindow(szClassName, szTitle, WS_OVERLAPPEDWINDOW |
		WS_CLIPCHILDREN | WS_CLIPSIBLINGS, 200, 250, 500, 120,
		HWND_DESKTOP, NULL, hThisInst, NULL);
	/* Отображение окна */
	ShowWindow(hWnd, nWinMode);
	UpdateWindow(hWnd);
	/* Цикл обработки сообщений */
	while (GetMessage(&msg, NULL, 0, 0)) // Получение сообщения
	{
		TranslateMessage(&msg); // Преобразование виртуальных кодов клавиш в ASCII-значения
		DispatchMessage(&msg); // Посылка сообщения в нужную оконную процедуру
	}
	return msg.wParam;
}