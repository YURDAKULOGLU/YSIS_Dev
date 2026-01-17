**Technical Specification (SPEC.md)**
=====================================

### Overview
-----------

This document outlines the technical requirements for implementing a new currency conversion service using a hardcoded rate. The purpose of this service is to convert USD to EUR, and it will be exposed via a new MCP tool called `convert_currency`.

### Requirements
--------------

#### Business Requirements

* Implement a new service that converts USD to EUR using a hardcoded rate.
* Expose the conversion service via a new MCP tool called `convert_currency`.
* The conversion service should return the converted amount in EUR.

#### Functional Requirements

* The service should accept USD as input and return the converted amount in EUR.
* The conversion rate is hardcoded for simplicity, but it may need to be updated periodically.
* The service should handle errors gracefully, such as invalid input or rate update issues.

### Rationale
-------------

The implementation of this new service will provide a simple way to convert USD to EUR using a fixed rate. This will enable the MCP tool `convert_currency` to offer users a convenient way to perform currency conversions.

### Technical Approach
----------------------

#### Service Implementation

* The currency conversion service will be implemented in Python using the Flask web framework.
* The service will use a simple function-based approach, with a single endpoint that accepts USD as input and returns the converted amount in EUR.
* The conversion rate will be hardcoded for simplicity, but it may need to be updated periodically.

#### MCP Tool Implementation

* The MCP tool `convert_currency` will be implemented using Flask as well.
* The tool will make an HTTP request to the currency conversion service endpoint to perform the conversion.
* The tool will handle errors and exceptions gracefully.

### Data Models and API Signatures
---------------------------------

#### Currency Conversion Service

| Method | URL | Request Body | Response |
| --- | --- | --- | --- |
| GET | /convert | - | { "eur": float } |

The currency conversion service will accept a single HTTP request with the USD amount as input, and it will return the converted amount in EUR.

#### MCP Tool

| Method | URL | Request Body | Response |
| --- | --- | --- | --- |
| GET | /convert | - | { "eur": float } |

The MCP tool `convert_currency` will make an HTTP request to the currency conversion service endpoint with the USD amount as input, and it will return the converted amount in EUR.

### Constraints and Considerations
-----------------------------------

#### Performance

* The currency conversion service should be able to handle a reasonable number of concurrent requests without significant performance degradation.
* The MCP tool `convert_currency` should be able to handle a large volume of requests per second without issues.

#### Scalability

* The currency conversion service should be designed to scale horizontally using multiple instances behind a load balancer.
* The MCP tool `convert_currency` should be designed to scale vertically, with the ability to increase its resources as needed.

#### Security

* The currency conversion service and MCP tool should implement proper authentication and authorization mechanisms to prevent unauthorized access.
* Any sensitive data, such as API keys or hardcoded rates, should be stored securely using environment variables or a secrets manager.

### Technical Debt
-----------------

This implementation assumes that the hardcoded conversion rate will be updated periodically. However, this may lead to technical debt if the update process is not properly managed. It's recommended to implement a more robust solution for updating the conversion rate in the future.

### Next Steps
--------------

1. Implement the currency conversion service and MCP tool according to the specifications outlined above.
2. Test the implementation thoroughly to ensure it meets all functional requirements.
3. Deploy the services to production and monitor their performance and scalability.
4. Regularly review and update the hardcoded conversion rate to prevent technical debt.