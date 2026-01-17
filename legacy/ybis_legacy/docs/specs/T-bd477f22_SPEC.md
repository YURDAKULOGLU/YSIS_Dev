# Technical Specification (SPEC.md)

## Task Objective
Implement a new service `src/ybis/services/currency.py` that converts USD to EUR using a hardcoded rate. Expose this service via a new MCP tool `convert_currency` in `mcp_server.py`.

## Requirements
### What needs to be built

* A Python service (`currency.py`) that takes two arguments: `amount` and `from_currency`, both of type `str`. The `from_currency` argument is expected to be "USD".
* The service uses a hardcoded conversion rate from USD to EUR.
* The service returns the converted amount as a float value.

### Why it's needed

* To provide a simple way to convert currency using a fixed conversion rate for testing and development purposes.
* To demonstrate the use of a Python service with MCP tooling.

## Technical Approach
### How

* Use Flask as the web framework for building the Python service.
* Define API endpoints using RESTful design principles.
* Implement the service logic in the `currency.py` file, including retrieving the hardcoded conversion rate and performing the conversion.
* Create a new MCP tool (`convert_currency`) in `mcp_server.py` that exposes the `currency` service.

## Data Models and API Signatures

### Currency Service (currency.py)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded conversion rate from USD to EUR
CONVERSION_RATE = 0.88

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    amount = float(data['amount'])
    from_currency = data['from_currency']

    if from_currency != 'USD':
        return jsonify({'error': 'Unsupported currency'}), 400

    converted_amount = amount * CONVERSION_RATE
    return jsonify({'converted_amount': converted_amount})

if __name__ == '__main__':
    app.run(debug=True)
```

### MCP Tool (mcp_server.py)
```python
from flask import Flask, request, jsonify
from currency import app

# Create a new route for the MCP tool
@app.route('/convert', methods=['POST'])
def mcp_convert_currency():
    return convert_currency()

if __name__ == '__main__':
    app.run(debug=True)
```

## Constraints and Considerations

* The conversion rate should be hardcoded in the `currency.py` file, as it will not change.
* The service should only accept USD as the from currency, to avoid support for other currencies.
* Error handling should be implemented for unsupported currencies or invalid request data.
* Security considerations: this implementation assumes that the MCP tool will only be used by trusted users. Consider implementing authentication and authorization mechanisms if exposing this service to external users.

This technical specification outlines the requirements, technical approach, data models, API signatures, and constraints for building a new Python service that converts USD to EUR using a hardcoded rate.