# List all the events in a Calendar

Used to list all the events in a Calendear.

**URL** : `/api/calendar/<calendar_id>/event`

**Method** : `GET`

**URL Parameters** : 
- `from` (Optional) : List all the events from this date (Format: YYYY-MM-DD HH:MM:SS)
- `until` (Optional) : List all the events until this date (Format: YYYY-MM-DD HH:MM:SS)

**Auth required** : YES - Basic Auth


**Request example**

```curl
curl -X GET \
  http://localhost:5000/api/calendar/1/event \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "events": [
        {
            "id": 2,
            "start_date": "2020-07-29 20:15:00",
            "end_date": "2020-07-29 21:15:00",
            "title": "Dinner",
            "description": "",
            "calendar": 1
        },
        {
            "id": 3,
            "start_date": "2020-06-22 14:15:00",
            "end_date": "2020-06-22 15:15:00",
            "title": "Pick Up Mom",
            "description": "At the Airport",
            "calendar": 1
        }
    ]
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