Django приложение для управления списком автомобилей, которые хранятся в базе данных PostgreSQL.
Для запуска сервера нужно собрать образ docker с помощью команды:
```bash
docker-compose build
```
и запусть контейнеры с помощью команды:
```bash
docker-compose up
```
проект car_management имеет Dockerfile для установки и запуска контейнера, в котором
endpoint.sh запускает Django приложение и делает миграции базы данных.

Файл переменных среды .env:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DB_TYPE = sqlite # or postgres отвечает за используемый тип базы данных
```
На страницах проекта можно использовать Django-формы для создания автомобилей и комментариев.
Для них определены роуты и представления.
Для API определены следующие роуты:
 - cars/: [GET, POST] список автомобилей, добавление нового автомобиля
 - cars/:id/ [GET, PUT, DELETE]: информация об автомобиле, обновление данных, удаление записи
 - cars/:id/comments/: [GET, POST] список комментариев к автомобилю, добавление нового комментария к автомобилю