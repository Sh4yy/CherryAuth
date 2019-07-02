# Cherry Auth
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
