# OPERATIONS

References:
- INTERFACES.md
- SECURITY.md

## Worker model
Workers claim leases, run workflows, write evidence, update DB, release leases.

## Leases
- TTL + heartbeat renewal
- expired => task re-queued
- abandoned runs remain as evidence

## Docker
docker-compose.yml provides:
- mcp service
- worker service
- optional redis profile for queue

