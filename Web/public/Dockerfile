# Используем официальный образ Node.js
FROM node:latest
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app
# Копируем зависимости
COPY package*.json .
# Устанавливаем зависимости
RUN npm install
# Устанавливаем Web-Server и пакет для параллельного запуска серверов
RUN npm install -g http-server concurrently
# Копируем все файлы в контейнер
COPY . .
# Задаём порт под сервер с веб-страницей
EXPOSE 8080
# Задаём порт под сервер, обрабатывающий комментарии
EXPOSE 3000
# Команда для запуска веб-сервера для отображения страницы и обработки комментариев
CMD concurrently "http-server -p 8080" "node server.js"
