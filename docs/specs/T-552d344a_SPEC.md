**SPEC.md**
===============

**Task Objective:** Implement a Currency Conversion Service
=====================================================

**Requirements**
---------------

### What needs to be built

* A Python service `src/ybis/services/currency.py` that converts USD to EUR using a hardcoded exchange rate.
* A new MCP tool `convert_currency` in `mcp_server.py` that exposes the currency conversion service.

### Rationale
-------------

The goal of this task is to provide a standardized way to convert currencies between USD and EUR, allowing for easy integration with other services. This will enable users to easily convert between these two widely used currencies.

**Technical Approach**
--------------------

* The `currency.py` service will use a simple hardcoded exchange rate for the conversion.
* The MCP tool `convert_currency` will be implemented using Flask, a lightweight web framework.
* The MCP server will use a RESTful API to expose the currency conversion service.

### Data Models and API Signatures
-------------------------------

#### Currency Conversion Service

* **Data Model:**
	+ Input: `USD_amount` (float)
	+ Output: `EUR_amount` (float) converted from USD_amount using the hardcoded exchange rate.
* **API Signature:**
```python
from flask import request, jsonify
from src.ybis.services.currency import CurrencyConverter

def convert_currency(USD_amount):
    # Hardcoded exchange rate
    exchange_rate = 0.89
    
    EUR_amount = USD_amount * exchange_rate
    return EUR_amount
```

#### MCP Tool Convert Currency

* **API Signature:**
```python
from flask import request, jsonify
from src.mcp_server import convert_currency_api

@app.route('/convert-currency', methods=['POST'])
def convert_currency_endpoint():
    data = request.get_json()
    USD_amount = data['USD_amount']
    EUR_amount = convert_currency(USD_amount)
    return jsonify({'EUR_amount': EUR_amount})
```

### Constraints and Considerations
---------------------------------

* The hardcoded exchange rate will be reviewed and updated periodically to ensure accuracy.
* The `currency.py` service should be refactored to use a database or external API for the exchange rate in the future.
* The MCP tool `convert_currency` should be tested thoroughly to ensure proper functionality and error handling.

### System Constraints
---------------------

* The system should scale horizontally to handle increasing traffic.
* The system should have a load balancer to distribute incoming requests evenly across multiple instances.
* The system should use a reverse proxy to handle SSL/TLS encryption for secure connections.