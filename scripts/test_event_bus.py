import asyncio
import sys
import os
from datetime import datetime

# Setup path
sys.path.insert(0, os.getcwd())
from src.agentic.infrastructure.redis_queue import event_bus, Events

async def event_listener():
    print("[TEST] Listener started... Waiting for events.")

    def on_event(event):
        print(f"[TEST] 🔔 EVENT RECEIVED: {event['type']} | Sender: {event['sender']}")
        print(f"[TEST] Payload: {event['data']}")

    # Start listening in background
    # Note: This will run for 10 seconds for the test
    try:
        await asyncio.wait_for(
            event_bus.subscribe_async([Events.TASK_CREATED, "test.manual"], on_event),
            timeout=5
        )
    except asyncio.TimeoutError:
        print("[TEST] Listener timeout (this is expected for the test)")

async def event_publisher():
    await asyncio.sleep(1) # Give listener a head start
    print("[TEST] Publisher sending event...")

    success = event_bus.publish(
        Events.TASK_CREATED,
        {"task_id": "TASK-E2E-TEST", "goal": "Verify Event Bus"}
    )

    if success:
        print("[TEST] ✅ Event published successfully!")
    else:
        print("[TEST] ❌ Event publication FAILED (is Redis running?)")

async def main():
    if not event_bus.available:
        print("[ERROR] Redis is not available. Please start Redis container.")
        return

    # Run both listener and publisher
    await asyncio.gather(
        event_listener(),
        event_publisher()
    )

if __name__ == "__main__":
    asyncio.run(main())
