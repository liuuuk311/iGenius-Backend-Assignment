# Get all Calendars

Used to get all calendars of a given user.


**URL** : `/api/user/<user_id>/calendar`

**Method** : `GET`

**Auth required** : YES - Basic Auth


**Request example**

```curl
curl -X GET \
  http://localhost:5000/api/user/2/calendar \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "calendars": [
        {
            "id": 3,
            "name": "Work",
            "description": "My Company Calendar",
            "created_at": "2020-01-25 17:40:53",
            "owner": 2
        },
        {
            "id": 4,
            "name": "Personal",
            "description": "My Own Calendar",
            "created_at": "2020-01-25 17:40:53",
            "owner": 2
        },
        {
            "id": 5,
            "name": "Family",
            "description": "",
            "created_at": "2020-01-25 17:40:53",
            "owner": 2
        }
    ]
}
```
---
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




[Back](../../README.md)