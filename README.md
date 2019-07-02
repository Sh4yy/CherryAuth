![Frame](https://user-images.githubusercontent.com/23535123/60550765-12eeb600-9cf7-11e9-92e8-06332c17f835.png)
A central authentication microservice

# Login
Create a new JWT token for a user.\
**Route**: `/login`\
**Method** : `GET`\
**Port** : `5001`\
**Authorization** : `Basic Auth` \
**Headers**:
```json
{
    "Authorization": "Basic [Basic Auth]"
}
```
**Response**:
```json
{
  "ok": true,
  "user_id": "user_id",
  "jwt": { 
    "refresh_token": "jwt refresh token",
    "token": "json web token",
    "payload": {
      "exp": 1532062978.3113165,
      "iat": 1532032978.3113165
    }},
  "timestamp": 1532032978.3113165
}
```

Note that user id should be used as username for basic auth
