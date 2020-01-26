# Login

Used to logged-in a user. If the user is not logged-in, the user cannot perform any action on its resource.

**URL** : `/api/user/login`

**Method** : `POST`

**Auth required** : NO

**Data example**

```json
{
    "email": "test@example.com",
    "password": "pwd"
}
```

**Request example**

```curl
curl -X POST \
  http://localhost:5000/api/user/login \
  -F email=test \
  -F password=pwd
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "User logged-in successfully",
    "user": {
        "id": 2,
        "created_at": "2020-01-25 17:40:53",
        "email": "test@example.com",
        "first_name": "Joe",
        "last_name": "Doe",
        "last_login": "2020-01-25 17:45:18",
        "status": "logged-in"
    }
}
```

## Error Response

**Condition** : If a user is already logged-in.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "User is already logged-in"
}
```
