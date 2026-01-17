**Specification**
=================

**Task Title:** Implement Currency Conversion Service

**Requirements**
---------------

### What Needs to be Built

1. A Python service (`src/ybis/services/currency.py`) that takes USD as input and returns EUR as output.
2. The service will use a hardcoded conversion rate.
3. A new MCP tool (`mcp_server.py`) that exposes the currency conversion service.

### Rationale

The goal of this task is to provide a simple, straightforward way to convert between major currencies (USD and EUR) using a hardcoded conversion rate. This will allow for easy testing and development of other currency conversion services in the future.

### Technical Approach

1. The `currency.py` service will use a simple dictionary-based approach to store the hardcoded conversion rates.
2. The `mcp_server.py` tool will be responsible for exposing the currency conversion service via a RESTful API.

### Data Models and API Signatures

#### Currency Conversion Service (`src/ybis/services/currency.py`)

* `convert_usd_to_eur( amount: float ) -> float `
 + Input parameters:
 - `amount`: The USD value to convert.
* Response format:
 - JSON response with the converted EUR value.

Example usage in `mcp_server.py`:
```python
from flask import Flask, jsonify
import currency

app = Flask(__name__)

@app.route('/convert_currency', methods=['POST'])
def convert_currency():
    data = request.get_json()
    amount_usd = data['amount']
    result = currency.convert_usd_to_eur(amount_usd)
    return jsonify({'eur': result})

if __name__ == '__main__':
    app.run(debug=True)
```

#### MCP Tool (`mcp_server.py`)

* The `convert_currency` service will be exposed via a RESTful API with the following endpoint:
 + `POST /convert_currency`
 + Request body: JSON object with the USD amount to convert.
 + Response format: JSON response with the converted EUR value.

### Constraints and Considerations

1. **Hardcoded conversion rates**: The use of hardcoded conversion rates may not be suitable for production environments where exchange rate changes need to be reflected in real-time.
2. **API Security**: The `convert_currency` service should be designed with security in mind, using HTTPS encryption and authentication mechanisms (e.g., API keys) as needed.
3. **Scalability**: The MCP tool should be designed to handle a high volume of requests without impacting performance.

### Next Steps

1. Implement the `currency.py` service with hardcoded conversion rates.
2. Develop the `mcp_server.py` tool to expose the currency conversion service via the MCP API.
3. Integrate the MCP tool with other services in the system, as needed.