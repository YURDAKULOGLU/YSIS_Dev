from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

from .security import authenticate_request

def create_response(status: str, message: str, data=None):
    """Create a standardized response."""
    response_data = {
        "status": status,
        "message": message
    }
    if data:
        response_data["data"] = data
    return jsonify(response_data), 200 if status == "success" else 400

app = Flask(__name__)


@app.route('/api/v1/bridge/send', methods=['POST'])
@authenticate_request
def send_message():
    """
    Send a message to the CrewAI Bridge.

    Request Body:
    ```json
    {
      "message": "string",
      "component": "string"
    }
    ```

    Response:
    ```json
    {
      "status": "success",
      "data": {
        "message": "Message sent",
        "component": "<component_name>"
      }
    }
    """
    try:
        data = request.json
        logging.info(f"Received message from client: {request.remote_addr}. Data: {data}")
        if not isinstance(data, dict) or 'message' not in data or 'component' not in data:
            error_message = "Geersiz istek gvdesi. Ltfen 'message' ve 'component' alanlarn ieren bir JSON nesnesi gnderin."
            logging.error(f"Error from client: {request.remote_addr}. {error_message}")
            return create_response("error", error_message)
        # Handle the incoming message and forward it to the appropriate AI component
        logging.info(f"Forwarding message to component: {data['component']} from client: {request.remote_addr}")
        response_data = {
            "message": data['message'],
            "component": data['component']
        }
        logging.info(f"Response to client: {request.remote_addr}. Data: {response_data}")
        return create_response("success", "Message sent", response_data)
    except Exception as e:
        logging.error(f"Mesaj ileme srasnda hata olutu (stemci IP: {request.remote_addr}): {str(e)}", exc_info=True)
        return create_response("error", f"Dahili sunucu hatas: {str(e)}")

@app.route('/api/v1/bridge/receive', methods=['POST'])
@authenticate_request
def receive_message():
    """
    Receive a message from the CrewAI Bridge.

    Request Body:
    ```json
    {
      "message": "string",
      "component": "string"
    }
    ```

    Response:
    ```json
    {
      "status": "success",
      "data": {
        "message": "Message received",
        "component": "<component_name>"
      }
    }
    """
    try:
        data = request.json
        logging.info(f"Received message from client: {request.remote_addr}. Data: {data}")
        if not isinstance(data, dict) or 'message' not in data or 'component' not in data:
            error_message = "Geersiz istek gvdesi. Ltfen 'message' ve 'component' alanlarn ieren bir JSON nesnesi gnderin."
            logging.error(f"Error from client: {request.remote_addr}. {error_message}")
            return create_response("error", error_message)
        # Handle the incoming message from an AI component
        logging.info(f"Message received from component: {data['component']} from client: {request.remote_addr}")
        response_data = {
            "message": data['message'],
            "component": data['component']
        }
        logging.info(f"Response to client: {request.remote_addr}. Data: {response_data}")
        return create_response("success", "Message received", response_data)
    except Exception as e:
        logging.error(f"Mesaj alma srasnda hata olutu (stemci IP: {request.remote_addr}): {str(e)}", exc_info=True)
        return create_response("error", f"Dahili sunucu hatas: {str(e)}")

if __name__ == '__main__':
    # Run the Flask application with debug mode disabled in production
    app.run(host='0.0.0.0', port=5000, debug=False)
