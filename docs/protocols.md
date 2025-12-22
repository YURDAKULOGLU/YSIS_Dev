# CrewAI Bridge Protocols

## API Endpoints

- **POST /api/v1/bridge/send**
  - **Description**: Send a message to the CrewAI Bridge.
  - **Request Body**:
    ```json
    {
      "message": "string",
      "component": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "data": {
        "message": "Message sent",
        "component": "<component_name>"
      }
    }
    ```

- **POST /api/v1/bridge/receive**
  - **Description**: Receive a message from the CrewAI Bridge.
  - **Request Body**:
    ```json
    {
      "message": "string",
      "component": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "data": {
        "message": "Message received",
        "component": "<component_name>"
      }
    }
    ```

## Security

- **Authentication**: All requests must include a valid `Authorization` header with a token.
- **Token Validation**: The server validates the token using JWT (JSON Web Token) and checks for expiration and validity.
- **Authorization**: The server ensures that the user has the necessary permissions to access the API endpoints. For example, only users with the 'admin' role can access certain resources.

## Data Structures

### Message
```json
{
  "message": "string",
  "component": "string"
}
```

## Logging

- **Logging Levels**: The server logs information at different levels (INFO, ERROR) to help with debugging and monitoring.
- **Log Format**: Logs include timestamps, the name of the logger, log level, and the message.

### Error Handling

- **Error Responses**: In case of errors, the server returns appropriate HTTP status codes along with a JSON response containing the error message.
- **Exception Logging**: All exceptions are logged with stack traces for detailed debugging.
