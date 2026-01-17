# SPEC.md
## Task Objective: Implement Currency Conversion Service

### Requirements

#### What needs to be built:

1. A Python service (`src/ybis/services/currency.py`) that converts USD to EUR using a hardcoded exchange rate.
2. Expose the conversion service via a new MCP (Multi-Protocol Client) tool, `convert_currency` in `mcp_server.py`.

#### Why it's needed:

1. The application requires a currency conversion feature for users.
2. To facilitate international transactions and data exchange.

### Technical Approach

#### Design Principles:

1. Use a modular design pattern to separate the conversion logic from the MCP exposure.
2. Employ a simple, yet efficient data structure (e.g., dictionary) to store hardcoded exchange rates.
3. Implement error handling for potential rate updates or invalid inputs.

#### Architecture Patterns:

1. Service-Oriented Architecture (SOA): The `currency.py` service will be a self-contained module, accessible via the MCP tool.
2. API Gateway Pattern: The MCP tool will act as an entry point to the conversion service.

### Data Models and API Signatures

#### Hardcoded Exchange Rates:

| Currency | Exchange Rate |
| --- | --- |
| USD    | 1.00        |

```python
# src/ybis/services/currency.py
exchange_rates = {
    'USD': 1.00,
    # Add more currencies as needed
}
```

#### API Signature (MCP Tool):

```python
# mcp_server.py
import requests

def convert_currency(amount: float, from_currency: str, to_currency: str):
    """
    Convert amount from one currency to another.

    Args:
        amount (float): The amount to be converted.
        from_currency (str): The original currency code (e.g., USD).
        to_currency (str): The target currency code (e.g., EUR).

    Returns:
        float: The converted amount.
    """
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        raise ValueError("Unsupported currency")

    rate = exchange_rates[from_currency] / exchange_rates[to_currency]
    return amount * rate
```

### Constraints and Considerations

1. **Hardcoded Rates:** Use a centralized location (e.g., `exchange_rates` dictionary) for hardcoded rates to ensure easy updates and management.
2. **Error Handling:** Implement robust error handling to handle invalid inputs, rate updates, or other potential issues.
3. **Scalability:** As the application grows, consider implementing a more scalable solution, such as using an external API or database to store exchange rates.
4. **Security:** Ensure that sensitive data (e.g., hardcoded rates) is stored securely and access is restricted to authorized parties.
5. **Maintainability:** Keep the conversion logic simple and well-documented to facilitate future maintenance and updates.

### Next Steps

1. Implement the `currency.py` service with the specified requirements.
2. Develop the MCP tool (`convert_currency`) in `mcp_server.py`, integrating the conversion service.
3. Conduct thorough testing and validation of the new feature.