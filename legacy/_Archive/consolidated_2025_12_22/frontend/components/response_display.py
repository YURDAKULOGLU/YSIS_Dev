from backend.services.memory_service import YBISMemoryService
import asyncio

memory_service = YBISMemoryService()

async def display_response(query):
    context = await memory_service.retrieve(query)
    if isinstance(context, list):
        context_str = "\n".join(context).strip()
    else:
        context_str = str(context).strip()
    
    response = await memory_service.generateResponse(query, [context_str])
    full_response = f"Context:\n{context_str}\n\nResponse:\n{response}"
    print(f"Query: {query}\n{full_response}")

# Örnek kullanım
# asyncio.run(display_response("example query"))
