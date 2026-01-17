# SPEC.md
## Task Objective: Implement Currency Conversion Service

### Requirements
#### What needs to be built:

1. **Currency Conversion Service**: A new service `src/ybis/services/currency.py` that takes USD as input and returns EUR after applying a hardcoded conversion rate.
2. **MCP Tool Integration**: Expose the currency conversion service via a new MCP tool `convert_currency` in `mcp_server.py`.

#### Why it's needed:
The implementation of this service is necessary to provide a centralized way to convert currencies, reducing the complexity of handling multiple conversion rates.

### Technical Approach
1. **Design Pattern**: This service will utilize the Strategy design pattern for handling different currency conversion rates.
2. **Database**: For storing and retrieving currency conversion rates, we will use a simple in-memory data store (e.g., Python dictionary) for development purposes. In production, consider using a more robust database solution.

### Data Models and API Signatures
#### Currency Conversion Service

* `src/ybis/services/currency.py`:
 + Function: `convert_currency(amount: float, from_currency: str, to_currency: str)`
    - Parameters:
      - `amount`: The amount to be converted (float)
      - `from_currency`: The currency to convert from (str, e.g., 'USD')
      - `to_currency`: The currency to convert to (str, e.g., 'EUR')
 + Return Value: Converted amount in the target currency (float)

#### MCP Tool Integration
* `mcp_server.py`:
 + Function: `convert_currency(amount: float, from_currency: str, to_currency: str)`
    - Parameters:
      - `amount`: The amount to be converted (float)
      - `from_currency`: The currency to convert from (str, e.g., 'USD')
      - `to_currency`: The currency to convert to (str, e.g., 'EUR')
 + Return Value: Converted amount in the target currency (float)

### Constraints and Considerations
1. **Hardcoded Rates**: Store conversion rates in a hardcoded dictionary within the `src/ybis/services/currency.py` module.
2. **API Security**: Implement basic input validation to prevent malicious requests from affecting the service's behavior.
3. **Error Handling**: Handle potential errors during conversion, such as insufficient funds or invalid currency codes.
4. **Code Organization**: Maintain a consistent naming convention and code structure throughout the `src/ybis/services/currency.py` module.

### Future Work
1. **Database Integration**: Consider migrating to a more robust database solution for storing and retrieving currency conversion rates.
2. **API Documentation**: Develop comprehensive API documentation for the MCP tool integration.
3. **Rate Update Mechanism**: Implement a mechanism for updating conversion rates in real-time or at scheduled intervals.