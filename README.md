# Note Management App Backend

API for Note Management application

![alt text](https://img.shields.io/badge/python-3.10.9-green)

## Development

### Up and build containers
```shell
docker-compose up -d --build
```

### Install poetry
```shell
pip install poetry
```
 
### Install the project dependencies
```shell
cd src && poetry install
```

### Spawn a shell within the virtual environment
```shell
poetry shell
```

### Run dev server
```shell
python manage.py runserver
```

### Import env 
```shell
export $(grep -v "^#" .env.local | xargs)
``` 
