## SPEC.md
### Task Objective: Implement Currency Conversion Service

**What Needs to Be Built**
---------------------------

* A Python service (`src/ybis/services/currency.py`) that takes a USD amount as input and returns the equivalent EUR value using a hardcoded exchange rate.
* The service will be exposed via a new MCP tool called `convert_currency` in `mcp_server.py`.

### Why It's Needed (Rationale)
-------------------------------

The implementation of a currency conversion service is necessary to provide a standardized way for users to convert between currencies, particularly USD and EUR. This feature will enhance the overall usability and flexibility of our application.

### Technical Approach
----------------------

* The service will utilize a simple arithmetic formula to calculate the exchange rate: `eur_value = usd_amount * hardcoded_rate`.
* The service will use a hardcoded rate for simplicity, but in a real-world scenario, this rate should be retrieved from an external data source (e.g., API) or database.
* To expose the service via MCP, we will use Flask, a lightweight web framework for Python.

### Data Models and API Signatures
---------------------------------

#### Currency Conversion Service

| HTTP Request | Parameter | Type | Required |
| --- | --- | --- | --- |
| `POST /convert_currency` | `amount_usd` | float | Yes |
| `GET /convert_currency` | `amount_usd` | float | No |

| HTTP Response | Code | Description |
| --- | --- | --- |
| 200 OK | `{"eur_value": float}` | Success response with EUR value |
| 400 Bad Request | - | Invalid request data |

#### MCP Tool convert_currency

```python
from flask import Flask, jsonify, request
import src.ybis.services.currency as currency_service

app = Flask(__name__)

@app.route('/convert_currency', methods=['POST'])
def convert_currency():
    amount_usd = float(request.json['amount_usd'])
    eur_value = currency_service.convert(amount_usd)
    return jsonify({'eur_value': eur_value})

if __name__ == '__main__':
    app.run(debug=True)
```

### Constraints and Considerations
------------------------------------

* The hardcoded exchange rate should be reviewed periodically to ensure its accuracy.
* To improve maintainability, we will consider using an external data source (e.g., API) to retrieve the exchange rate in a future iteration.
* We will follow established design principles, such as KISS (Keep it Simple, Stupid) and YAGNI (You Ain't Gonna Need It), when implementing this service.

### Future Improvements
-----------------------

* Integrate an external data source for the exchange rate to improve accuracy and reduce maintenance burden.
* Consider using a more robust arithmetic formula or algorithm to handle edge cases (e.g., division by zero).
* Implement additional features, such as error handling and logging, to enhance the overall robustness of the service.