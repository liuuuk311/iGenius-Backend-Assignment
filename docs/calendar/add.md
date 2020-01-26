# Add new Calendar

Used to create a new Calendar for a given user.

**URL** : `/api/user/<user_id>/calendar`

**Method** : `POST`

**Auth required** : YES - Basic Auth

**Data example**

```json
{
    "name": "Work",
    "description": "My Company Calendar"
}
```

**Request example**

```curl
curl -X POST \
  http://localhost:5000/api/user/1/calendar \
  -H 'Authorization: Basic cGlwcG9AdG9ubmEuY29tOnBhc3N3b3Jk' \
  -F name=Work \
  -F 'description=My Company Calendar'
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "Calendar created successfully",
    "calendar": {
        "id": 2,
        "name": "Work",
        "description": "My Company Calendar",
        "created_at": "2020-01-25 17:40:53",
        "owner": 1
    }
}
```

## Error Response

**Condition** : If the user is not logged-id.

**Code** : `401 UNAUTHORIZED`

**Content** :

```json
{
    "status": "error",
    "message": "User is not logged-in"
}
```

**Condition** : If <user_id> does not match with the client.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
    "status": "error",
    "message": "Cannot access at this resource"
}
```

**Condition** : If <user_id> does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "status": "error",
    "message": "User does not exists"
}
```

[Back](../../README.md)