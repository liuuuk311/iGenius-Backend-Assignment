# Update an Event

Used to update a given Event.

**URL** : `/api/event/<event_id>`

**Method** : `PUT`


**Auth required** : YES - Basic Auth

**Data example**

```json
{
    "start_date":"2020-07-29 16:15:00",
    "end_date":"2020-07-29 17:15:00",
    "title":"Meeting",
    "description":"",
    "calendar_id": 1
}
```

**Request example**

```curl
curl -X PUT \
  http://localhost:5000/api/event/2 \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
  -F 'start_date=2020-07-29 16:15:00' \
  -F 'end_date=2020-07-29 17:15:00' \
  -F title=Meeting \
  -F description= \
  -F calendar_id=1
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "Event updated successfully"
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