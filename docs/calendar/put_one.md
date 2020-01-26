# Update Calendar

Used to update a given Calendar.

**URL** : `/api/calendar/<calendar_id>`

**Method** : `PUT`

**Auth required** : YES - Basic Auth


**Request example**

```curl
curl -X PUT \
  http://localhost:5000/api/calendar/3 \
  -H 'Authorization: Basic dGVzdDpwd2Q=' \
  -F name=Work \
  -F 'description=New Description'
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "message": "Calendar updated successfully"
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