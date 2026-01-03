import subprocess

def retrieve_memory(query: str) -> str:
    """Call the TypeScript retrieveMemory function via a subprocess."""
    result = subprocess.run(
        ["node", "-e", f"require('./structure').retrieveMemory('{query}')"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
