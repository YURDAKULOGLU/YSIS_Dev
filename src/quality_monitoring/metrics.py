import json

# Load quality thresholds from config file
with open('config/code_quality_thresholds.json', 'r') as f:
    quality_thresholds = json.load(f)

def check_code_quality(metrics):
    """
    Check if the code metrics are within the defined quality thresholds.
    
    Args:
        metrics (dict): A dictionary containing code metrics such as complexity, cyclomatic_complexity, maintainability_index, lines_of_code.
        
    Returns:
        bool: True if all metrics are within thresholds, False otherwise.
    """
    for metric, value in metrics.items():
        threshold = quality_thresholds.get(metric)
        if threshold is not None and value > threshold:
            print(f"Code quality regression detected: {metric} ({value}) exceeded threshold ({threshold})")
            return False
    return True

# Example usage
if __name__ == "__main__":
    example_metrics = {
        "complexity": 8,
        "cyclomatic_complexity": 4,
        "maintainability_index": 75,
        "lines_of_code": 450
    }
    
    if check_code_quality(example_metrics):
        print("Code quality is within acceptable thresholds.")
    else:
        print("Code quality issues detected.")
