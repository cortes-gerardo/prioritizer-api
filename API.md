# API Documentation
## Introduction

## Getting Started
- Base URL: at the moment the code runs at `https://prioritizer-api.herokuapp.com`
- Authentication: Authentication to the API is performed via HTTP Basic Auth. Provide your `JWT` as the basic auth value.
 login using the credentials in [Auth0 login](https://cortes-gerardo.us.auth0.com/authorize?audience=prioritizer&response_type=token&client_id=VsDbNuQQopNlsE60IPR4HoYrVmzQ62Wi&redirect_uri=http://localhost:8080/authorize) to generate the `JWT`

please store this value as shown to run the following cURL
```sh
export JWT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imp1SkE3RnI4NXFkLXJCRVc4QkxYYiJ9.eyJpc3MiOiJodHRwczovL2NvcnRlcy1nZXJhcmRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzYjBjZDJhZDMyYzAwMTM0ZmY2NGUiLCJhdWQiOiJwcmlvcml0aXplciIsImlhdCI6MTU5Njg2NzQ4MiwiZXhwIjoxNTk2OTUzODgyLCJhenAiOiJWc0RiTnVRUW9wTmxzRTYwSVBSNEhvWXJWbXpRNjJXaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnNwcmludCIsImRlbGV0ZTp0YXNrIiwicGF0Y2g6c3ByaW50IiwicGF0Y2g6dGFzayIsInBvc3Q6c3ByaW50IiwicG9zdDp0YXNrIl19.d1kWv3v2p5YQCeQBdYzetYwLTGmefdffDQ2WYIwLSIqDf3hh0uKoxNFnreov1kfkR0IB3ardyGmCzpscKtDhEJO18XoT-e-VqtEk1zWWwOtE8RgiupwNSbLYVm_G0yPVlHAUJ5dYPcp9y_aLPN4JbOqaoA71qCAJW6YhnTuaUxsH4To0RZCva3SDrTkVNsCsNkg__RreN9mnYF58s_vfP5oUSAsBHy6obyKhiYzmBz2gFw8E_dcMmYPXmhBhmIw3vZpeh2iFUjr0dguwrb5DQacNAAfI06iAwLnJXloxfLr5LJd4OZrorSlOTvdYh1aFWnobwwsD6uE5GG6wohvVbA
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
curl https://prioritizer-api.herokuapp.com/sprints
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprints": [
    {
      "duration": 14,
      "goal": "finish Capstone project",
      "id": 1,
      "tasks": 9
    }
  ],
  "success": true
}
```

### POST /sprints
Adds a new sprint

###### Example Request: 
```sh
curl https://prioritizer-api.herokuapp.com/sprints \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "goal": "this is a goal",
    "start_date": "2020-08-08",
    "end_date": "2020-08-16"
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprint": {
    "id": 2,
    "goal": "this is a goal",
    "duration": 8,
    "tasks": 0
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
curl https://prioritizer-api.herokuapp.com/sprints/2 \
-X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "goal": "this is an edited goal",
    "start_date": "2020-08-08",
    "end_date": "2020-08-24"
}'
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "sprint": {
    "id": 2,
    "goal": "this is an edited goal",
    "duration": 16,
    "tasks": 0
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
curl https://prioritizer-api.herokuapp.com/sprints/2 \
-X DELETE \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}"
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true,
  "deleted_sprint": 2
}
```

### GET /sprints/{{sprint_id}}/tasks
Shows all the tasks from the sprint specified in the URL

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl https://prioritizer-api.herokuapp.com/sprints/2/tasks
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true,
  "necessity": [],
  "productivity": [],
  "distraction": [
    {
      "description": "check all emails",
      "done": false,
      "id": 35,
      "important": false,
      "urgent": true
    }
  ],
  "waste": []
}
```

### POST /sprints/{{sprint_id}}/tasks
Adds a new task to the sprint specified in the URL

##### Path variables:
**sprint_id** `integer`

###### Example Request: 
```sh
curl https://prioritizer-api.herokuapp.com/sprints/2/tasks \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
    "description": "check all emails",
    "important": false,
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
    "id": 35,
    "description": "check all emails",
    "important": false,
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
curl https://prioritizer-api.herokuapp.com/tasks/35 \
-X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}" \
-d '{
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
    "id": 35,
    "description": "check all emails",
    "important": false,
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
curl https://prioritizer-api.herokuapp.com/tasks/35 \
-X DELETE \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ${JWT}"
```

###### Example Response:
Header: `Content-Type: application/json`

Body:
```json
{
  "success": true,
  "deleted_task": 35
}
```
