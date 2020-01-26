# Add new Event

Used to create a new Event in a given calendar.

**URL** : `/api/calendar/<calendar_id>/event`

**Method** : `POST`

**Auth required** : YES - Basic Auth

**Data example**

```json
{
    "start_date":"2020-07-29 18:15:00",
    "end_date":"2020-07-29 19:15:00",
    "title":"Meeting",
    "description":"New opportunity",
}
```

**Request example**

```curl
curl -X POST \
  http://localhost:5000/api/calendar/1/event \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
  -F 'start_date=2020-07-29 18:15:00' \
  -F 'end_date=2020-07-29 19:15:00' \
  -F title=Meeting \
  -F 'description=New opportunity'
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "Event created successfully",
    "event": {
        "id": 1,
        "start_date": "2020-07-29 18:15:00",
        "end_date": "2020-07-29 19:15:00",
        "title": "Meeting",
        "description": "New opportunity",
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

**Condition** : If <calendar_id> does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "status": "error",
    "message": "Calendar does not exists"
}
```

[Back](../../README.md)