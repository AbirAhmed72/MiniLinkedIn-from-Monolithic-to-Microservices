Here's my docker-compose.yaml file. whenever i run `docker-compose up`, it returns `Error response from daemon: invalid volume specification:` Heres the docker-compose.yaml file-

```
    version: '3.8'

    services:

        nginx:
            build:
                context: ./nginx
            restart: always
            ports:
                - "80:80"
            depends_on:
                - user_service


        user_service:
            build:
                context: ./user_service
            restart: always
            container_name: user_service_container
            ports:
                - "8000:8000"
            depends_on:
                - user_db
            environment:
                DATABASE_URL: postgresql://postgres:1234@user_db:5432/User

        user_db:
            image: postgres:16.0
            container_name: user_db_container
            environment:
                POSTGRES_USER: postgres
                POSTGRES_PASSWORD: 1234
                POSTGRES_DB: User
            restart: always
            ports:
                - "5432:5432"
            volumes:
                - ./init/user_service_init.sql:/docker-entrypoint-initdb.d/user_service_init.sql
                - user_db_data:/var/lib/postgresql/data

    volumes:
        user_db_data:

```
this is my folder structure currently-
project_directory/
|-- docker-compose.yml
|-- init/
|   |-- user_service_init.sql
|   |-- post_service_init.sql
|   |-- notification_service_init.sql
|-- user_service/
|   |-- Dockerfile
|   |-- ... (other files for your user service)
|-- post_service/
|   |-- Dockerfile
|   |-- ... (other files for your post service)
|-- notification_service/
|   |-- Dockerfile
|   |-- ... (other files for your notification service)
|-- nginx/
|   |-- Dockerfile
|   |-- ... (other files for your nginx service)
|-- ... (other project files and directories)

here's my sql file which is inside init folder(init/user_service_init.sql):

```
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password_hashed VARCHAR
);

```

and below is the full error that im getting:
[![error image](https://i.stack.imgur.com/E2KdZ.png)](https://i.stack.imgur.com/E2KdZ.png)


I tried googling and also tried looking in stackoverflow but did not find any specific solution.