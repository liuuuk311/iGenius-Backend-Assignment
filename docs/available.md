# List all the events of a User

Used to list all the events for a given User.

**URL** : `/api/user/<user_id>/available`

**Method** : `GET`

**URL Parameters** : 
The following parameters are mandatory
- `from`: Check availabilty from this date (Format: YYYY-MM-DD HH:MM:SS)
- `until`: Check availabilty until this date (Format: YYYY-MM-DD HH:MM:SS)

**Auth required** : NO


**Request example**

```curl
curl -X GET \
  'http://localhost:5000/api/user/1/available?from=2020-02-01%2010:00:00&until=2020-02-01%2012:00:00' \
```

## Success Response

**Code** : `200 OK`

**Response Content example**

```json
{
    "status": "ok",
    "is_available": "true"
}
```

## Error Response

**Condition** : If <user_id> does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "status": "error",
    "message": "User does not exists"
}
```

[Back](../README.md)