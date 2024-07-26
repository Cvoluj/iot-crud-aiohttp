# IoT CRUD

## Installation
1. Clone the repository.
2. `cp .env.example .env`
3. Fill .env file and generate or write own 32-digit `SECRET_KEY`
4. `make app`
5. Go on localhost:${PORT}

Examples of requests in Postman, Insomnia, etc:

```POST http://localhost:8080/users```
```
{
  Request:
  "name": "john doe",
  "email": "john.doe@example.com",
  "password": "password123"
}
```
As result new user will be created <br>
```POST http://localhost:8080/login```
```
Request:
{
  "email": "john.doe@example.com",
  "password": "password123"
}
```
 
```
Response
{
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5fQ.XQoPNLOZxmtw8wobfT7_G0RsVOVEfooEB-fL0M7MKg0"
}
```
Use this token with Bearer auth. Now you logged in and can use more endpoint: <br>
```PUT http://localhost:8080/users/1```
```
Request:
{
	"name": "2.com"
}
```
```
Response:
{
	"id": 1,
	"name": "2.com",
	"email": "john.doe@example.com",
	"created_at": "2024-07-25T19:11:50.896249",
	"updated_at": "2024-07-25T19:11:50.896249"
}
```
```DELETE http://localhost:8080/users/1``` <br>
You will delete your user

```POST http://localhost:8080/location```
```
Request
{
	"name": "home"
}
```
```
Response
{
    "id": 1,
    "name": "home",
    "api_user_id": 1,
}
```
```GET http://localhost:8080/location/1```
```
{
	"id": 1,
	"name": "home",
	"api_user_id": 1
}
```

Other endpoint not realized yet

