# Technical Specification (SPEC.md)

## Task Objective
Fix the syntax error in `src/ybis/services/currency.py`

## Rationale
The current implementation of the currency service has a syntax error that needs to be addressed. This fix is crucial to ensure the stability and maintainability of the system.

## Technical Approach

*   **Code Review**: Conduct a thorough review of the `currency.py` file to identify the source of the syntax error.
*   **Syntax Correction**: Apply the necessary corrections to the code, ensuring that the syntax is accurate and consistent with established coding standards.
*   **Unit Testing**: Write unit tests to validate that the corrected code functions as expected.

## Data Models and API Signatures

*   The `Currency` data model remains unchanged, as there are no changes required to its structure. For reference, please see `src/ybis/models/currency.py`.
*   No API signature changes are necessary; however, updated documentation will be provided to ensure clarity on the expected usage of the corrected service.

## Constraints and Considerations

*   **Code Duplication**: Avoid duplicating code in the future by utilizing established patterns (e.g., using an existing currency converter library instead of rolling out one's own solution).
*   **Dependency Updates**: Ensure that all dependencies are up-to-date to prevent compatibility issues.
*   **Testing Coverage**: Implement comprehensive unit tests to guarantee thorough coverage and catch any regressions introduced during the fix.

## Acceptance Criteria

1.  The syntax error in `src/ybis/services/currency.py` is corrected.
2.  The code adheres to standard coding conventions (PEP 8).
3.  Unit tests validate that the corrected service functions as expected.

## Timeline
The task is estimated to take approximately 2 hours to complete, assuming a single developer will work on this task.