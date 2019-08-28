![Frame](https://user-images.githubusercontent.com/23535123/60550765-12eeb600-9cf7-11e9-92e8-06332c17f835.png)
A central authentication microservice
The purpose for this app is to have a generic authentication service that could be intergrated in all sorts of applications!

# Routes
## Register
Register a new User/Identity.\
**Route**: `/v1/register`\
**Method** : `POST`\
**Port** : `5001`\
**Authorization** : `Basic Auth` \
**Headers**:
```json
{
    "Authorization": "Basic YTI5ODhjYTIwOWFkMDkwN2QzYWY5YzFjM2I3YWNiMWU6ZG9udHVzZXRoaXNwYXNzd29yZA=="
}
```
**Response**:
```json
{
    "uid": "a2988ca209ad0907d3af9c1c3b7acb1e",
    "reg_date": 1562184696,
    "ok": true,
    "timestamp": 1562184696.5919928551
}
```
**Possiple Errors**

```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If User/Identity Already Exist.
Code: `400 BAD REQUEST`
Message: `user already exist`
```

## Login
Create a new JWT token for a User/Identity.\
**Route**: `/v1/login`\
**Method** : `GET`\
**Port** : `5001`\
**Authorization** : `Basic Auth` \
**Headers**:
```json
{
    "Authorization": "Basic YTI5ODhjYTIwOWFkMDkwN2QzYWY5YzFjM2I3YWNiMWU6ZG9udHVzZXRoaXNwYXNzd29yZA=="
}
```
**Response**:
```json
{
    "jwt": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJmMTJkMDEwZTIyOGU5NTY5OGZmNzk5MTY5MzRjM2VlMyIsImlhdCI6MTU2MjE4NTA1NSwiZXhwIjoxNTYyMTg4NjU1LCJ1aWQiOiJhMjk4OGNhMjA5YWQwOTA3ZDNhZjljMWMzYjdhY2IxZSJ9.Y0FHxuBcZLJvUMp49ZQa49Z5F6XwKubyBNA5hcnNSrw",
        "refresh_token": "226c1a30f26c9af6a825b29d4204990e43446e5bab690d5134ddd70ab20725f2",
        "payload": {
            "sid": "f12d010e228e95698ff79916934c3ee3",
            "iat": 1562185055,
            "exp": 1562188655,
            "uid": "a2988ca209ad0907d3af9c1c3b7acb1e"
        }
    },
    "uid": "a2988ca209ad0907d3af9c1c3b7acb1e",
    "ok": true,
    "timestamp": 1562185055.7063784599
}
```

**Possiple Errors**

```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If User/Identity does not exist.
Code: `404 Not Found`
Message: `user does not exist`
```
```
If Credentials are not correct.
Code: `401 Unauthorized`
Message: `incorrect credentials`
```

## Logout
Terminate a session for a User.\
**Route**: `/v1/logout`\
**Method** : `POST`\
**Port** : `5001`\
**Authorization** : `Bearer Auth` \
**Headers**:
```json
{
    "Authorization": "Bearer 226c1a30f26c9af6a825b29d4204990e43446e5bab690d5134ddd70ab20725f2"
}
```
**Response**:
```json
{
    "logged_out": true,
    "token": "226c1a30f26c9af6a825b29d4204990e43446e5bab690d5134ddd70ab20725f2",
    "uid": "a2988ca209ad0907d3af9c1c3b7acb1e",
    "ok": true,
    "timestamp": 1562185790.1397087574
}
```

**Possiple Errors**

```
If authorization method is not Bearer.
Code: `400 BAD REQUEST`
Message: `invalid authorization method`
```
```
If authorization header is missing the token.
Code: `400 BAD REQUEST`
Message: `invalid authorization token`
```
```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If Session does not exist.
Code: `404 Not Found`
Message: `session does not exist`
```
```
If Credentials are not correct.
Code: `401 Unauthorized`
Message: `incorrect credentials`
```

Note that for logout, instead of passing the JWT token in the Authorization header, the refresh token must be passed.

## Refersh Token
Refreshing a JWT token after its expired.\
**Route**: `/v1/token/refresh`\
**Method** : `GET`\
**Port** : `5001`\
**Authorization** : `Bearer Auth` \
**Headers**:
```json
{
    "Authorization": "Bearer 226c1a30f26c9af6a825b29d4204990e43446e5bab690d5134ddd70ab20725f2"
}
```
**Response**:
```json
{
    "jwt": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJhODY2YTZmODQxNjY5YTcyOTg0YjAwNTVlYWNiMDU5ZCIsImlhdCI6MTU2MjE4NjE0OSwiZXhwIjoxNTYyMTg5NzQ5LCJ1aWQiOiJhMjk4OGNhMjA5YWQwOTA3ZDNhZjljMWMzYjdhY2IxZSJ9.qKseJAKOQjH_3cTQsRQwuAhwHIdAnMos27weGxUsNUY",
        "refresh_token": "f2617cabda2b1d88c7002a985c79e30d8b77277a06aca4382b4fab08553728ae",
        "payload": {
            "sid": "a866a6f841669a72984b0055eacb059d",
            "iat": 1562186149,
            "exp": 1562189749,
            "uid": "a2988ca209ad0907d3af9c1c3b7acb1e"
        }
    },
    "uid": "a2988ca209ad0907d3af9c1c3b7acb1e",
    "ok": true,
    "timestamp": 1562186149.7159590721
}
```

**Possiple Errors**

```
If authorization method is not Bearer.
Code: `400 BAD REQUEST`
Message: `invalid authorization method`
```
```
If authorization header is missing the token.
Code: `400 BAD REQUEST`
Message: `invalid authorization token`
```
```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If Session does not exist.
Code: `404 Not Found`
Message: `session does not exist`
```

Note that for Refreshing the JWT token, instead of passing the JWT token in the Authorization header, the refresh token must be passed.

## Changing Password
Changing a User's password.\
**Route**: `/v1/password/change`\
**Method** : `POST`\
**Port** : `5001`\
**Authorization** : `Basic Auth` \
**Headers**:
```json
{
    "Authorization": "Basic YTI5ODhjYTIwOWFkMDkwN2QzYWY5YzFjM2I3YWNiMWU6ZG9udHVzZXRoaXNwYXNzd29yZA=="
}
```
**Request Body**
```json
{
	"new_password": "new password here",
	"kill_sessions": false
}
```
**Response**:
```json
{
    "changed_password": true,
    "killed_sessions": false,
    "ok": true,
    "timestamp": 1562186437.9157345295
}
```

**Possiple Errors**

```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If User does not exist.
Code: `404 Not Found`
Message: `session does not exist`
```
```
If Credentials are not correct.
Code: `401 Unauthorized`
Message: `incorrect credentials`
```

Note that for this route, kill_session is an optional body field which will kill every active session for this user if is set to True. Also, old password must be passed with user id as basic authorization header

## Verify JWT Token
 verify a user's jwt token.\
**Route**: `/v1/verify`\
**Method** : `POST`\
**Port** : `5001`\
**Authorization** : `Bearer Auth` \
**Headers**:
```json
{
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJhODY2YTZmODQxNjY5YTcyOTg0YjAwNTVlYWNiMDU5ZCIsImlhdCI6MTU2MjE4NTYxMiwiZXhwIjoxNTYyMTg5MjEyLCJ1aWQiOiJhMjk4OGNhMjA5YWQwOTA3ZDNhZjljMWMzYjdhY2IxZSJ9.72dUB4p4g_L3Bx6UpqQZMCVn3So2Bn7K2xulDWFRJEQ"
}
```
**Response**:
```json
{
    "valid": true,
    "payload": {
        "sid": "a866a6f841669a72984b0055eacb059d",
        "iat": 1562185612,
        "exp": 1562189212,
        "uid": "a2988ca209ad0907d3af9c1c3b7acb1e"
    },
    "ok": true,
    "timestamp": 1562186902.8546676636
}
```

**Possiple Errors**

```
If missing authorization header.
Code: `400 BAD REQUEST`
Message: `missing authorization header`
```
```
If authorization method is not Bearer.
Code: `400 BAD REQUEST`
Message: `invalid authorization method`
```
```
If authorization header is missing the token.
Code: `400 BAD REQUEST`
Message: `invalid authorization token`
```
```
If JWT token is Expired.
Code: `401 Unauthorized`
Message: `expired signature`
```
```
If JWT token has an invalid signature.
Code: `401 Unauthorized`
Message: `invalid signature`
```
```
Other possible JWT errors.
Code: `401 Unauthorized`
Message: `invalid token`
```





















