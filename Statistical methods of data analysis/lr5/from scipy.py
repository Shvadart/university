import random

def generate_matrix_game(m, n):
    """
    Генерирует произвольную матричную игру с значениями от 0 до 10.

    Args:
        m: Число стратегий первого игрока.
        n: Число стратегий второго игрока.

    Returns:
        Кортеж (A, m, n), где A - матрица игры, m - число стратегий первого игрока, n - число стратегий второго игрока.
        Возвращает None, если не удалось сгенерировать игру без доминирующих строк/столбцов.
    """

    while True:
        A = [[random.uniform(0, 10) for _ in range(n)] for _ in range(m)]

        # Проверка на отсутствие доминирующих строк
        dominated_rows = []
        for i in range(m):
            for j in range(m):
                if i != j and all(A[i][k] <= A[j][k] for k in range(n)):
                    dominated_rows.append(i)
                    break
            if len(dominated_rows) > 0:
                break  # Выходим из внутреннего цикла, если строка доминирована

        if len(dominated_rows) > 0:
            continue

        # Проверка на отсутствие доминирующих столбцов
        dominated_cols = []
        for j in range(n):
            for k in range(n):
                if j != k and all(A[i][j] <= A[i][k] for i in range(m)):
                    dominated_cols.append(j)
                    break
            if len(dominated_cols) > 0:
                break  # Выходим из внутреннего цикла, если столбец доминирован


        if len(dominated_cols) > 0:
            continue
        return (A, m, n)


# Пример использования:
m = 4  # Число стратегий первого игрока
n = 5  # Число стратегий второго игрока

game_data = generate_matrix_game(m, n)

if game_data:
    A, m, n = game_data
    print("Матрица игры:")
    for row in A:
        print(row)
    print("Число стратегий первого игрока:", m)
    print("Число стратегий второго игрока:", n)
else:
    print("Не удалось сгенерировать игру без доминирующих строк/столбцов. Попробуйте другие значения m и n.")