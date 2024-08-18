# TODO Application API

This API provides the full fledged of action that helps developer to build a their own todo application using any client side framwork. It has lot of functionality such as all CRUD opertiona, task management and other associated fucntionality stuff.

## Command to start the application using docker 🚀👌

```bash
    docker-compose up --build
```

it expose the port 80 of localhost and you can access the application from there. Before starting application ensure that you migrate the models in the database. To migrate the models

```bash
    docker-compose -f docker-compose.html exec api python manage.py migrate
```

## Command for start the application using Terminal 👏👌

1. make the virtual environment

```bash
    python -m venv venv
```

2. activate the virtual environment

```bash
    press ctrl+shif+p and select python interpreter and choose the venv environment
```

3. run the migrations

```bash
    python manage.py migrate
```

4. start the server

```bash
    python manage.py runserver
```
