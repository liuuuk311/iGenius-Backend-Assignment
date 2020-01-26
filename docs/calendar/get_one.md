# Get one Calendar

Used to get one specific calendar.


**URL** : `/api/calendar/<calendar_id>`

**Method** : `GET`

**Auth required** : YES - Basic Auth


**Request example**

```curl
curl -X GET \
  http://localhost:5000/api/calendar/3 \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "calendar": {
        "id": 3,
        "name": "Work",
        "description": "My Company Calendar",
        "created_at": "2020-01-25 17:40:53",
        "owner": 2
    }
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

**Condition** : If owner of the calendar does not match with the client.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
    "status": "error",
    "message": "Cannot access at this resource"
}
```

**Condition** : If <calendar_id> does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "status": "error",
    "message": "Calendar not found"
}
```


[Back](../../README.md)