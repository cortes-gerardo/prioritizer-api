# API Documentation
## Introduction

## Getting Started
- Base URL: at the moment the code runs locally at `http://0.0.0.0:8080/`
- Authentication: Authentication to the API is performed via HTTP Basic Auth. Provide your `JWT` as the basic auth value.
 login using the credentials in [Auth0 login](https://cortes-gerardo.us.auth0.com/authorize?audience=prioritizer&response_type=token&client_id=VsDbNuQQopNlsE60IPR4HoYrVmzQ62Wi&redirect_uri=http://localhost:8080/authorize) to generate the `JWT`

please store this value as shown to run the following cURL
```sh
export JWT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imp1SkE3RnI4NXFkLXJCRVc4QkxYYiJ9.eyJpc3MiOiJodHRwczovL2NvcnRlcy1nZXJhcmRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzYjBjZDJhZDMyYzAwMTM0ZmY2NGUiLCJhdWQiOiJwcmlvcml0aXplciIsImlhdCI6MTU5NTY0NjY4MiwiZXhwIjoxNTk1NzMzMDgyLCJhenAiOiJWc0RiTnVRUW9wTmxzRTYwSVBSNEhvWXJWbXpRNjJXaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnNwcmludCIsImRlbGV0ZTp0YXNrIiwicGF0Y2g6c3ByaW50IiwicGF0Y2g6dGFzayIsInBvc3Q6c3ByaW50IiwicG9zdDp0YXNrIl19.Ao_vqcJ2fCdpzPgQDO9-5zi2USHfqtEe32u6KAOUPeXs2Xc2v5lY3Xpyq_R3jhI38vFXz82Qr85xQbfD3lyjqu5gsm3yagvPOcnmlyQDRV3k07VfrtrvC7ehZiP0QZD0uafLrtGrgGY2avXdUoRIoanJBZw-a_Idq_9MOUKOQQrLr9ZV3y1JMrp8eDrIAsk5SqhRy7UFpysFfHMkQS1ZCszMxtYTl1boklhJS69czAYmbnBT19C_hpPiIsBdvIvIShta9H_J12t0eWsDpeXp51FcbvkhQkuZF3AbevzZ8erO_hBLJnoAMZhNXOuhMz_8bz08vEvGjbJ-mPbp1HF39Q
```

## Error Handling
Errors are returned as a `JSON` object, it contains three field
 - **success** as a `boolean` set in `false`
 - **error** an `integer` with the HTTP status code
 - **message** as the HTTP status code name as `String`

For authentication and authorization exceptions, two more fields are included
 - **code** as a classification of the exception
 - **description** specifying what the exception is about

Example Response:
```json
{
  "success": false,
  "error": 401, 
  "message": "Unauthorized", 
  "code": "authorization_header_missing", 
  "description": "Authorization header is expected."
}
```

The API will return these status codes when the request fails

|         HTTP status code |                                                           |
| -----------------------: | --------------------------------------------------------- |
|        400 - Bad Request | Please check the body, for typos in the field names       |
| 404 - Resource Not Found | The id selected does not exist                            |
|    422 - Not Processable | unique constrain violated                                 |
|       401 - Unauthorized | No valid token provided in the header                     |
|          403 - Forbidden | The token does not have permission to perform the request |

some expected error codes are:

|                  Error types |                                                            |
| ---------------------------: | ---------------------------------------------------------- |
| authorization_header_missing | The Authorization header in not included                   |
|               invalid_header | The header format should be `Authorization: Bearer ${JWT}` |
|               invalid_claims | JWT info is not for this API                               |
|                 unauthorized | The token does not have permission to perform the request  |
|                token_expired | The token is not valid anymore                             |

## Endpoints
### GET /sprints
Shows all the sprints stored

###### Example Request:
```sh
curl http://0.0.0.0:8080/sprints
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprints": [
    {
      "id": 248,
      "goal": "edited goal",
      "start_date": "Fri, 24 Jul 2020 00:00:00 GMT",
      "end_date": "Fri, 31 Jul 2020 00:00:00 GMT"
    }
  ],
  "success": true
}
```

### POST /sprints
Adds a new sprint

###### Example Request: 
```sh
curl http://0.0.0.0:8080/sprints \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "goal": "this is a goal",
    "start_date": "2020-07-12",
    "end_date": "2020-07-19"
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprint": {
    "id": 248,
    "goal": "this is a goal",
    "start_date": "Sun, 12 Jul 2020 00:00:00 GMT",
    "end_date": "Sun, 19 Jul 2020 00:00:00 GMT"
  },
  "success": true
}
```

### PATCH /sprints/{{sprint_id}}
Edit all or individual fields of the sprint

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/sprints/248 \
-X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "goal": "edited goal",
    "start_date": "2020-07-24",
    "end_date": "2020-07-31"
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprint": {
    "id": 248,
    "goal": "edited goal",
    "start_date": "Fri, 24 Jul 2020 00:00:00 GMT",
    "end_date": "Fri, 31 Jul 2020 00:00:00 GMT"
  },
  "success": true
}
```

### DELETE /sprints/{{sprint_id}}
Deletes a sprint by id

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/sprints/248 \
-X DELETE \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}"
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
```

### GET /sprints/{{sprint_id}}/tasks
Shows all the tasks from the sprint specified in the URL

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/sprints/248/tasks
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 243,
      "description": "check all emails",
      "important": true,
      "urgent": true,
      "done": false
    }
  ]
}
```

### POST /sprints/{{sprint_id}}/tasks
Adds a new task to the sprint specified in the URL

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/sprints/248/tasks \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "description": "check all emails",
    "important": true,
    "urgent": true,
    "done": false
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true, 
  "task": {
    "id": 243, 
    "description": "check all emails", 
    "important": true, 
    "urgent": true,
    "done": false
  }
}
```

### PATCH /tasks/{{task_id}}
Edit one or all the fields from a task

##### Path variables:
**task_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/tasks/243 \
-X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "description": "check all emails",
    "important": true,
    "urgent": true,
    "done": true
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true,
  "task": {
    "id": 243,
    "description": "check all emails",
    "important": true,
    "urgent": true,
    "done": true
  }
}
```

### DELETE /tasks/{{task_id}}
Delete a task with only the id

##### Path variables:
**task_id** `integer`

###### Example Request: 
```sh
curl http://0.0.0.0:8080/tasks/243 \
-X DELETE \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}"
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
```
