# ⚖️ ARTICLE 1: THE PRIME DIRECTIVES

## 1.1 The "Dog Scales Dog" Philosophy
We are not just building a product; we are building the **factory** that builds the product.
*   **Improve the Process:** If a task is repetitive, do not just do it. Build an agent or script to do it forever.
*   **Self-Correction:** The system must include mechanisms (auditors) to check its own integrity.

## 1.2 The Iron Chain of Truth
Information flows in one direction only. This prevents hallucinations and drift.

```mermaid
graph TD
    A[PRD (Problem)] --> B[Architecture (Solution)]
    B --> C[Specs (Blueprint)]
    C --> D[Code (Brick)]
    D --> E[Tests (Verification)]
```

*   **Rule:** You cannot write Code without a Spec. You cannot write a Spec without Architecture.
*   **Enforcement:** The `verify-doc-integrity.py` auditor will block actions if this chain is broken.

## 1.3 Think Twice, Code Once
*   **No Cowboy Coding:** Unplanned code is legacy code.
*   **Docs are Code:** Documentation is not an afterthought; it is the *source code* of the logic. The actual `.py` or `.ts` files are just compiled byproducts of the documentation.
