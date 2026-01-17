# MIGRATIONS

References:
- CONSTITUTION.md
- INTERFACES.md

## Rules
- schema_version everywhere (tasks, runs, reports, META.json)
- migrations are idempotent
- never rewrite old run folders (read-time compatibility)

## Required
- migration registry
- migrate.check / migrate.apply commands
- migration produces a migration_report.json when executed in a run

