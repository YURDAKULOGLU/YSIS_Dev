# Redis Event Bus Adapter

References:
- ../adapters/README.md
- ../../configs/adapters.yaml

**Type:** Event Bus Adapter  
**Maturity:** Beta  
**Default Enabled:** No

## Overview
Redis-backed event bus for observability and async signaling.

## Installation
```bash
pip install -e ".[adapters-redis]"
```

## Configuration
```yaml
event_bus:
  enabled: true
  adapter: "redis"
adapters:
  redis_event_bus:
    enabled: true
```

## Notes
- Requires a local Redis instance when enabled.
- System runs without event bus if disabled.
