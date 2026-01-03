# Propagation Test Script for YBIS Self-Replication Process

import subprocess

def run_propagation_tests():
    """
    Execute the self-replication script and verify the results.
    """

    # Step 1: Run the self-replication script
    try:
        subprocess.run(
            [r"scripts\self_replicate.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("[OK] Self-replication script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Self-replication failed: {e.stderr}")
        return False

    # Step 2: Verify the replicated system consistency
    try:
        subprocess.run(
            ["scripts\verify_replication.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("[OK] Replicated system verified successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Verification failed: {e.stderr}")
        return False

    # Step 3: Document findings
    with open(r"docs\self_replication_process.md", "a") as f:
        f.write("\n## Propagation Test Results\n")
        f.write("- Self-replication script executed successfully.\n")
        f.write("- Replicated system verified successfully.\n")

    return True

if __name__ == "__main__":
    run_propagation_tests()
