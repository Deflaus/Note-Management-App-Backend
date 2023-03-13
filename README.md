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

### Run tests
```shell
pytest
```

## Start server

### Start dev server
```shell
docker-compose up -d --build

pip install poetry
cd src && poetry install
poetry shell

python manage.py runserver
```

### Use via swagger

1. Go to http://localhost:8000/api/docs/
2. After sign_up or sign_in use the token from the response body and place it in the Authorize form with the pattern 

```
Token {your_token}
```

3. Use swagger

### Use via curl

1. Sign up 

```shell
curl -X 'POST' \
  'http://localhost:8000/api/auth/sign_up/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "password": "string"
}'
```

Response body
```json
{
  "pk": 1,
  "username": "string",
  "is_active": true,
  "token": "95bf3f893540a8743710cee91afe7ae20542c4f4"
}
```

After sign_up use the token from the response body and place it in the Authorization header with the pattern 

```
Token {your_token}
```

2. Create note
```shell
curl -X 'POST' \
  'http://localhost:8000/api/notes/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "description": "string"
}'
```

Response body

```json
{
  "pk": 1,
  "name": "string",
  "description": "string",
  "created_at": "2023-03-13T08:25:21.876016Z"
}
```

3. Get own notes

```shell
curl -X 'GET' \
  'http://localhost:8000/api/notes/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token'
```

Response body

```json
[
  {
    "pk": 1,
    "name": "string",
    "description": "string",
    "created_at": "2023-03-13T08:25:21.876016Z"
  }
]
```

4. Get own note by id = 1
```shell
curl -X 'GET' \
  'http://localhost:8000/api/notes/1/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token'
```

Response body

```json
{
  "pk": 1,
  "name": "string",
  "description": "string",
  "created_at": "2023-03-13T08:25:21.876016Z"
}
```

5. Update own note by id = 1

```shell
curl -X 'PATCH' \
  'http://localhost:8000/api/notes/1/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "description": "string"
}'
```

Response body

```json
{
  "pk": 1,
  "name": "string",
  "description": "string",
  "created_at": "2023-03-13T08:25:21.876016Z"
}
```

6. Delete own note by id

```shell
curl -X 'DELETE' \
  'http://localhost:8000/api/note/1/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token' \
```

Response body - no body

7. Sign in

```shell
curl -X 'POST' \
  'http://localhost:8000/api/auth/sign_in/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "password": "string"
}'
```

Response body
```json
{
  "pk": 1,
  "username": "string",
  "is_active": true,
  "token": "95bf3f893540a8743710cee91afe7ae20542c4f4"
}
```

After sign_in use the token from the response body and place it in the Authorization header with the pattern 

```
Token {your_token}
```

8. Sign out
```shell
curl -X 'POST' \
  'http://localhost:8000/api/auth/sign_out/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token your_token'
```

Response body - no body