# sentinel.py

def execute_task(task):
    """
    Execute a given task.
    
    :param task: A callable representing the task to be executed.
    """
    try:
        result = task()
        print(f"Task executed successfully. Result: {result}")
    except Exception as e:
        print(f"An error occurred while executing the task: {e}")

# Example usage
if __name__ == "__main__":
    def sample_task():
        return "Hello, World!"
    
    execute_task(sample_task)