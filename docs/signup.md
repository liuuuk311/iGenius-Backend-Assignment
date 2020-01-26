# Signup

Create a new user.

**URL** : `/api/user/signup`

**Method** : `POST`

**Auth required** : NO

**Data example**

```json
{
    "first_name": "Joe",
    "last_name": "Doe",
    "email": "test@example.com",
    "password": "pwd"
}
```

**Request example**

```curl
curl -X POST \
  http://localhost:5000/api/user/signup \
  -F first_name=Joe \
  -F last_name=Doe \
  -F email=test@example.com \
  -F password=pwd
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "User created successfully",
    "user": {
        "id": 1,
        "created_at": "2020-01-25 17:40:53",
        "email": "test@example.com",
        "first_name": "Joe",
        "last_name": "Doe",
        "last_login": null,
        "status": "logged-out"
    }
}
```

## Error Response

**Condition** : If 'email' is already in use.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "Cannot create user",
    "details": "Email already in use"
}
```