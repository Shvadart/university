#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>

void list_files_with_extension(const char *path, const char *extension) {
    struct dirent *entry;
    struct stat info;
    DIR *dir = opendir(path);

    if (dir == NULL) {
        printf("Could not open directory: %s\n", path);
        return;
    }

    // Перебираем все элементы в текущем каталоге
    while ((entry = readdir(dir)) != NULL) {
        char filepath[256];
        snprintf(filepath, sizeof(filepath), "%s/%s", path, entry->d_name);

        if (stat(filepath, &info) != 0) {
            printf("Could not get file information: %s\n", filepath);
            continue;
        }

        if (S_ISDIR(info.st_mode)) {
            // Если это подкаталог, пропускаем его "." и ".."
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;

            // Рекурсивно вызываем эту функцию для подкаталога
            list_files_with_extension(filepath, extension);
        } else {
            // Если это файл с заданным расширением, выводим его имя
            if (strstr(entry->d_name, extension) != NULL)
                printf("%s\n", entry->d_name);
        }
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <extension>\n", argv[0]);
        return 1;
    }

    char *extension = argv[1];
    char current_dir[256];

    // Получаем текущий каталог
    if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
        printf("Could not get current directory\n");
        return 1;
    }

    // Повторяем действия до корневого каталога
    while (strcmp(current_dir, "/") != 0) {
        // Выводим имена файлов с заданным расширением в текущем каталоге
        list_files_with_extension(current_dir, extension);

        // Получаем родительский каталог и делаем его текущим
        snprintf(current_dir, sizeof(current_dir), "%s/..", current_dir);
        if (chdir(current_dir) != 0) {
            printf("Could not change to parent directory\n");
            return 1;
        }
    }

    return 0;
}