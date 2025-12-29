Steps to execute:
1. Run lite check on a completed task (archived):
   python scripts/protocol_check.py --task-id TASK-New-4130 --mode lite --auto-archive
2. Run full check on a completed task with full artifacts:
   python scripts/protocol_check.py --task-id TASK-New-6383 --mode full --auto-archive
3. Run lite check for this task:
   python scripts/protocol_check.py --task-id TASK-New-7503 --mode lite
4. Record outputs in artifacts/RESULT.md and update META.json.
