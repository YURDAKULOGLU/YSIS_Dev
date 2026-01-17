**Technical Specification (SPEC.md)**

# Currency Conversion Service
=====================================

## Requirements
-------------

The following requirements outline the needs of the currency conversion service:

### Functionality

*   Convert USD to EUR using a hardcoded exchange rate.
*   Expose the conversion service via a new MCP tool called `convert_currency`.

### Input Parameters

| Name | Type | Description |
| --- | --- | --- |
| amount | float | The amount of USD to convert. |

### Output Parameters

| Name | Type | Description |
| --- | --- | --- |
| converted_amount | float | The converted amount in EUR. |

## Rationale
-------------

The currency conversion service is needed to provide a simple and straightforward way for users to convert US dollars to euros without having to rely on external APIs or services.

## Technical Approach
--------------------

### Architecture Pattern

*   **Service-Oriented Architecture (SOA)**: The currency conversion service will be designed as a self-contained service, with its own input parameters, output parameters, and any necessary dependencies.
*   **Singleton Pattern**: Since the exchange rate is hardcoded, we can take advantage of the singleton pattern to ensure that only one instance of the currency converter is created.

### Code Structure

The `currency.py` file will contain a class-based implementation of the conversion service. This class will have two methods: `convert` and `get_rate`. The `convert` method takes in an amount, converts it using the hardcoded rate, and returns the converted amount. The `get_rate` method returns the hardcoded exchange rate.

### MCP Integration

The `mcp_server.py` file will expose the `convert_currency` function as a new endpoint on the MCP server. This function will take in an amount and convert it to EUR using the currency converter service.

## Data Models and API Signatures
---------------------------------

### Currency Converter Service (currency.py)

```python
class CurrencyConverter:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CurrencyConverter, cls).__new__(cls)
            cls._instance.rate = 0.88  # Hardcoded exchange rate for USD to EUR
        return cls._instance

    def convert(self, amount: float) -> float:
        """Converts the given amount from USD to EUR."""
        return amount * self.rate

    def get_rate(self) -> float:
        """Returns the hardcoded exchange rate for USD to EUR."""
        return self.rate
```

### MCP Server (mcp_server.py)

```python
from fastapi import FastAPI, HTTPException
from src.ybis.services.currency import CurrencyConverter

app = FastAPI()

@app.get("/convert_currency")
async def convert_currency(amount: float):
    """Exposes the currency conversion service."""
    converter = CurrencyConverter()
    converted_amount = converter.convert(amount)
    return {"converted_amount": converted_amount}
```

## Constraints and Considerations
---------------------------------

### Data Consistency

*   The hardcoded exchange rate should be reviewed regularly to ensure it remains accurate.
*   In a production environment, consider using an external data source for the exchange rate.

### Scalability

*   Since the conversion service is self-contained, it can be scaled independently of other services in the system.

### Maintainability

*   Following established patterns (e.g., singleton pattern) will make it easier to maintain and extend the currency conversion service.
*   Using a class-based implementation ensures that all necessary dependencies are accounted for.