# Logout

Used to logged-out a user.

**URL** : `/api/user/logout`

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
  http://localhost:5000/api/user/logout \
  -F email=test \
  -F password=pwd
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "User logged out successfully"
}
```

## Error Response

**Condition** : If a user is already logged-out.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "User is already logged-out"
}
```
[Back](../README.md)
