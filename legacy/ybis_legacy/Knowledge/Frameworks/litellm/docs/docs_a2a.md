Agent Gateway (A2A Protocol) - Overview | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Add A2A Agents on LiteLLM AI Gateway, Invoke agents in A2A Protocol, track request/response logs in LiteLLM Logs. Manage which Teams, Keys can access which Agents onboarded.

![](/assets/ideal-img/a2a_gateway.6f8c840.640.png)

  
  

| Feature | Supported |
| --- | --- |
| Supported Agent Providers | A2A, Vertex AI Agent Engine, LangGraph, Azure AI Foundry, Bedrock AgentCore, Pydantic AI |
| Logging | ✅ |
| Load Balancing | ✅ |
| Streaming | ✅ |

tip

LiteLLM follows the [A2A (Agent-to-Agent) Protocol](https://github.com/google/A2A) for invoking agents.

## Adding your Agent[​](#adding-your-agent "Direct link to Adding your Agent")

### Add A2A Agents[​](#add-a2a-agents "Direct link to Add A2A Agents")

You can add A2A-compatible agents through the LiteLLM Admin UI.

1. Navigate to the **Agents** tab
2. Click **Add Agent**
3. Enter the agent name (e.g., `ij-local`) and the URL of your A2A agent

![](/assets/ideal-img/add_agent_1.1c8f231.640.png)

The URL should be the invocation URL for your A2A agent (e.g., `http://localhost:10001`).

### Add Azure AI Foundry Agents[​](#add-azure-ai-foundry-agents "Direct link to Add Azure AI Foundry Agents")

Follow [this guide, to add your azure ai foundry agent to LiteLLM Agent Gateway](/docs/providers/azure_ai_agents#litellm-a2a-gateway)

### Add Vertex AI Agent Engine[​](#add-vertex-ai-agent-engine "Direct link to Add Vertex AI Agent Engine")

Follow [this guide, to add your Vertex AI Agent Engine to LiteLLM Agent Gateway](/docs/providers/vertex_ai_agent_engine)

### Add Bedrock AgentCore Agents[​](#add-bedrock-agentcore-agents "Direct link to Add Bedrock AgentCore Agents")

Follow [this guide, to add your bedrock agentcore agent to LiteLLM Agent Gateway](/docs/providers/bedrock_agentcore#litellm-a2a-gateway)

### Add LangGraph Agents[​](#add-langgraph-agents "Direct link to Add LangGraph Agents")

Follow [this guide, to add your langgraph agent to LiteLLM Agent Gateway](/docs/providers/langgraph#litellm-a2a-gateway)

### Add Pydantic AI Agents[​](#add-pydantic-ai-agents "Direct link to Add Pydantic AI Agents")

Follow [this guide, to add your pydantic ai agent to LiteLLM Agent Gateway](/docs/providers/pydantic_ai_agent#litellm-a2a-gateway)

## Invoking your Agents[​](#invoking-your-agents "Direct link to Invoking your Agents")

Use the [A2A Python SDK](https://pypi.org/project/a2a/) to invoke agents through LiteLLM.

This example shows how to:

1. **List available agents** - Query `/v1/agents` to see which agents your key can access
2. **Select an agent** - Pick an agent from the list
3. **Invoke via A2A** - Use the A2A protocol to send messages to the agent

invoke\_a2a\_agent.py

```
from uuid import uuid4  
import httpx  
import asyncio  
from a2a.client import A2ACardResolver, A2AClient  
from a2a.types import MessageSendParams, SendMessageRequest  
  
# === CONFIGURE THESE ===  
LITELLM_BASE_URL = "http://localhost:4000"  # Your LiteLLM proxy URL  
LITELLM_VIRTUAL_KEY = "sk-1234"             # Your LiteLLM Virtual Key  
# =======================  
  
async def main():  
    headers = {"Authorization": f"Bearer {LITELLM_VIRTUAL_KEY}"}  
      
    async with httpx.AsyncClient(headers=headers) as client:  
        # Step 1: List available agents  
        response = await client.get(f"{LITELLM_BASE_URL}/v1/agents")  
        agents = response.json()  
          
        print("Available agents:")  
        for agent in agents:  
            print(f"  - {agent['agent_name']} (ID: {agent['agent_id']})")  
          
        if not agents:  
            print("No agents available for this key")  
            return  
          
        # Step 2: Select an agent and invoke it  
        selected_agent = agents[0]  
        agent_id = selected_agent["agent_id"]  
        agent_name = selected_agent["agent_name"]  
        print(f"\nInvoking: {agent_name}")  
          
        # Step 3: Use A2A protocol to invoke the agent  
        base_url = f"{LITELLM_BASE_URL}/a2a/{agent_id}"  
        resolver = A2ACardResolver(httpx_client=client, base_url=base_url)  
        agent_card = await resolver.get_agent_card()  
        a2a_client = A2AClient(httpx_client=client, agent_card=agent_card)  
          
        request = SendMessageRequest(  
            id=str(uuid4()),  
            params=MessageSendParams(  
                message={  
                    "role": "user",  
                    "parts": [{"kind": "text", "text": "Hello, what can you do?"}],  
                    "messageId": uuid4().hex,  
                }  
            ),  
        )  
        response = await a2a_client.send_message(request)  
        print(f"Response: {response.model_dump(mode='json', exclude_none=True, indent=4)}")  
  
if __name__ == "__main__":  
    asyncio.run(main())
```

### Streaming Responses[​](#streaming-responses "Direct link to Streaming Responses")

For streaming responses, use `send_message_streaming`:

invoke\_a2a\_agent\_streaming.py

```
from uuid import uuid4  
import httpx  
import asyncio  
from a2a.client import A2ACardResolver, A2AClient  
from a2a.types import MessageSendParams, SendStreamingMessageRequest  
  
# === CONFIGURE THESE ===  
LITELLM_BASE_URL = "http://localhost:4000"  # Your LiteLLM proxy URL  
LITELLM_VIRTUAL_KEY = "sk-1234"             # Your LiteLLM Virtual Key  
LITELLM_AGENT_NAME = "ij-local"             # Agent name registered in LiteLLM  
# =======================  
  
async def main():  
    base_url = f"{LITELLM_BASE_URL}/a2a/{LITELLM_AGENT_NAME}"  
    headers = {"Authorization": f"Bearer {LITELLM_VIRTUAL_KEY}"}  
      
    async with httpx.AsyncClient(headers=headers) as httpx_client:  
        # Resolve agent card and create client  
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)  
        agent_card = await resolver.get_agent_card()  
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)  
  
        # Send a streaming message  
        request = SendStreamingMessageRequest(  
            id=str(uuid4()),  
            params=MessageSendParams(  
                message={  
                    "role": "user",  
                    "parts": [{"kind": "text", "text": "Hello, what can you do?"}],  
                    "messageId": uuid4().hex,  
                }  
            ),  
        )  
          
        # Stream the response  
        async for chunk in client.send_message_streaming(request):  
            print(chunk.model_dump(mode="json", exclude_none=True))  
  
if __name__ == "__main__":  
    asyncio.run(main())
```

## Tracking Agent Logs[​](#tracking-agent-logs "Direct link to Tracking Agent Logs")

After invoking an agent, you can view the request logs in the LiteLLM **Logs** tab.

The logs show:

* **Request/Response content** sent to and received from the agent
* **User, Key, Team** information for tracking who made the request
* **Latency and cost** metrics

![](/assets/ideal-img/agent2.eba7fcd.640.png)

## API Reference[​](#api-reference "Direct link to API Reference")

### Endpoint[​](#endpoint "Direct link to Endpoint")

```
POST /a2a/{agent_name}/message/send
```

### Authentication[​](#authentication "Direct link to Authentication")

Include your LiteLLM Virtual Key in the `Authorization` header:

```
Authorization: Bearer sk-your-litellm-key
```

### Request Format[​](#request-format "Direct link to Request Format")

LiteLLM follows the [A2A JSON-RPC 2.0 specification](https://github.com/google/A2A):

Request Body

```
{  
  "jsonrpc": "2.0",  
  "id": "unique-request-id",  
  "method": "message/send",  
  "params": {  
    "message": {  
      "role": "user",  
      "parts": [{"kind": "text", "text": "Your message here"}],  
      "messageId": "unique-message-id"  
    }  
  }  
}
```

### Response Format[​](#response-format "Direct link to Response Format")

Response

```
{  
  "jsonrpc": "2.0",  
  "id": "unique-request-id",  
  "result": {  
    "kind": "task",  
    "id": "task-id",  
    "contextId": "context-id",  
    "status": {"state": "completed", "timestamp": "2025-01-01T00:00:00Z"},  
    "artifacts": [  
      {  
        "artifactId": "artifact-id",  
        "name": "response",  
        "parts": [{"kind": "text", "text": "Agent response here"}]  
      }  
    ]  
  }  
}
```

## Agent Registry[​](#agent-registry "Direct link to Agent Registry")

Want to create a central registry so your team can discover what agents are available within your company?

Use the [AI Hub](/docs/proxy/ai_hub) to make agents public and discoverable across your organization. This allows developers to browse available agents without needing to rebuild them.

* [Adding your Agent](#adding-your-agent)
  + [Add A2A Agents](#add-a2a-agents)
  + [Add Azure AI Foundry Agents](#add-azure-ai-foundry-agents)
  + [Add Vertex AI Agent Engine](#add-vertex-ai-agent-engine)
  + [Add Bedrock AgentCore Agents](#add-bedrock-agentcore-agents)
  + [Add LangGraph Agents](#add-langgraph-agents)
  + [Add Pydantic AI Agents](#add-pydantic-ai-agents)
* [Invoking your Agents](#invoking-your-agents)
  + [Streaming Responses](#streaming-responses)
* [Tracking Agent Logs](#tracking-agent-logs)
* [API Reference](#api-reference)
  + [Endpoint](#endpoint)
  + [Authentication](#authentication)
  + [Request Format](#request-format)
  + [Response Format](#response-format)
* [Agent Registry](#agent-registry)