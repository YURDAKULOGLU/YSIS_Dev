Introduction - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Getting Started

Introduction

[Home](/)[Documentation](/en/introduction)[AOP](/en/enterprise/introduction)[API Reference](/en/api-reference/introduction)[Examples](/en/examples/example)[Changelog](/en/changelog)

* [Website](https://crewai.com)
* [Forum](https://community.crewai.com)
* [Blog](https://blog.crewai.com)
* [CrewGPT](https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant)

##### Getting Started

* [Introduction](/en/api-reference/introduction)
* [GET

  GET /inputs](/en/api-reference/inputs)
* [POST

  POST /kickoff](/en/api-reference/kickoff)
* [POST

  POST /resume](/en/api-reference/resume)
* [GET

  GET /{kickoff\_id}/status](/en/api-reference/status)

# [​](#crewai-aop-api) CrewAI AOP API

Welcome to the CrewAI AOP API reference. This API allows you to programmatically interact with your deployed crews, enabling integration with your applications, workflows, and services.

## [​](#quick-start) Quick Start

1

Get Your API Credentials

Navigate to your crew’s detail page in the CrewAI AOP dashboard and copy your Bearer Token from the Status tab.

2

Discover Required Inputs

Use the `GET /inputs` endpoint to see what parameters your crew expects.

3

Start a Crew Execution

Call `POST /kickoff` with your inputs to start the crew execution and receive
a `kickoff_id`.

4

Monitor Progress

Use `GET /{kickoff_id}/status` to check execution status and retrieve results.

## [​](#authentication) Authentication

All API requests require authentication using a Bearer token. Include your token in the `Authorization` header:

Copy

Ask AI

```
curl -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  https://your-crew-url.crewai.com/inputs
```

### [​](#token-types) Token Types

| Token Type | Scope | Use Case |
| --- | --- | --- |
| **Bearer Token** | Organization-level access | Full crew operations, ideal for server-to-server integration |
| **User Bearer Token** | User-scoped access | Limited permissions, suitable for user-specific operations |

You can find both token types in the Status tab of your crew’s detail page in
the CrewAI AOP dashboard.

## [​](#base-url) Base URL

Each deployed crew has its own unique API endpoint:

Copy

Ask AI

```
https://your-crew-name.crewai.com
```

Replace `your-crew-name` with your actual crew’s URL from the dashboard.

## [​](#typical-workflow) Typical Workflow

1. **Discovery**: Call `GET /inputs` to understand what your crew needs
2. **Execution**: Submit inputs via `POST /kickoff` to start processing
3. **Monitoring**: Poll `GET /{kickoff_id}/status` until completion
4. **Results**: Extract the final output from the completed response

## [​](#error-handling) Error Handling

The API uses standard HTTP status codes:

| Code | Meaning |
| --- | --- |
| `200` | Success |
| `400` | Bad Request - Invalid input format |
| `401` | Unauthorized - Invalid bearer token |
| `404` | Not Found - Resource doesn’t exist |
| `422` | Validation Error - Missing required inputs |
| `500` | Server Error - Contact support |

## [​](#interactive-testing) Interactive Testing

**Why no “Send” button?** Since each CrewAI AOP user has their own unique crew
URL, we use **reference mode** instead of an interactive playground to avoid
confusion. This shows you exactly what the requests should look like without
non-functional send buttons.

Each endpoint page shows you:

* ✅ **Exact request format** with all parameters
* ✅ **Response examples** for success and error cases
* ✅ **Code samples** in multiple languages (cURL, Python, JavaScript, etc.)
* ✅ **Authentication examples** with proper Bearer token format

### [​](#to-test-your-actual-api:) **To Test Your Actual API:**

## Copy cURL Examples

Copy the cURL examples and replace the URL + token with your real values

## Use Postman/Insomnia

Import the examples into your preferred API testing tool

**Example workflow:**

1. **Copy this cURL example** from any endpoint page
2. **Replace `your-actual-crew-name.crewai.com`** with your real crew URL
3. **Replace the Bearer token** with your real token from the dashboard
4. **Run the request** in your terminal or API client

## [​](#need-help) Need Help?

[## Enterprise Support

Get help with API integration and troubleshooting](/cdn-cgi/l/email-protection#7f0c0a0f0f100d0b3f1c0d1a081e16511c1012)[## Enterprise Dashboard

Manage your crews and view execution logs](https://app.crewai.com)

Was this page helpful?

YesNo

[GET /inputs

Next](/en/api-reference/inputs)

⌘I