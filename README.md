# API Documentation

## Open Endpoints

Open endpoints require no Authentication.

* [Signup](docs/signup.md) : `POST /api/user/signup/`
* [Login](docs/login.md) : `POST /api/user/login/`
* [Logout](docs/logout.md) : `POST /api/user/logout/`
* [Availability](docs/available.md) : `GET /api/user/<user_id>/available/`

## Endpoints that require Authentication

Closed endpoints require a valid username and password to be included in the header of the request as Basic Authentication. The username (email) and password must be valid. 

## Error Response
If the wrong credentials are used in the Authentication an error message will be returned.

**Condition** : Wrong credential in the Authentication Header.

**Code** : `401 UNAUTHORIZED`

**Content** :

```json
{
    "status": "error",
    "message": "Unauthorized request, please authenticate"
}
```

### Calendar actions

Each endpoint manipulates or displays information related to the Calendar of the user that is provided with the authentication in the request:

* [Create](docs/calendar/add.md) : `POST /api/user/<user_id>/calendar`
* [List All](docs/calendar/get_all.md) : `GET /api/user/<user_id>/calendar`
* [Get One](docs/calendar/get_one.md) : `GET /api/calendar/<calendar_id>`
* [Edit One](docs/calendar/put_one.md) : `PUT /api/calendar/<calendar_id>`
* [Remove](docs/calendar/delete.md) : `DELETE /api/calendar/<calendar_id>`

### Event actions

Endpoints for viewing and manipulating the Events of a given Calendar

* [Create](docs/event/add.md) : `POST /api/calendar/<calendar_id>/event`
* [List of a User's Events](docs/event/get_all_from_user.md) : `GET /api/user/<user_id>/event`
* [List of a Calendar's Events](docs/event/get_all_from_calendar.md) : `GET /api/calendar/<calendar_id>/event`
* [Get One](docs/event/get_one.md) : `GET /api/event/<event_id>` 
* [Edit One](docs/event/put_one.md) : `PUT /api/event/<calendar_id>`
* [Remove](docs/event/delete.md) : `DELETE /api/event/<event_id>`
user/<int:user_id>/
