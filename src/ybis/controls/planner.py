import json
import logging
import time

logger = logging.getLogger(__name__)


def exponential_backoff_request(request_function, max_retries=5, backoff_factor=2):
    retries = 0
    while retries < max_retries:
        try:
            response = request_function()
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Attempt {retries + 1} failed: {e}")
            wait_time = backoff_factor ** retries
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retries += 1
    raise Exception("All retries failed")

def create_plan():
    plan = {
        "exponential_backoff": {
            "max_retries": 5,
            "backoff_factor": 2
        }
    }
    return json.dumps(plan, indent=4)

if __name__ == "__main__":
    plan_json = create_plan()
    print(plan_json)
