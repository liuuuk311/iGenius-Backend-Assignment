# List all the events of a User

Used to list all the events for a given User.

**URL** : `/api/event/<event_id>`

**Method** : `GET`


**Auth required** : YES - Basic Auth


**Request example**

```curl
curl -X GET \
  http://localhost:5000/api/event/2 \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "event": {
        "id": 2,
        "start_date": "2020-07-29 20:15:00",
        "end_date": "2020-07-29 21:15:00",
        "title": "Dinner",
        "description": "",
        "calendar": 1
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

**Condition** : If <event_id> does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "status": "error",
    "message": "Event does not exists"
}
```

[Back](../../README.md)