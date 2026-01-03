import json

def parse_plan(json_string):
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing plan: {e}")

# Example usage
json_input = '{"property": "value"}'
try:
    parsed_data = parse_plan(json_input)
    print(parsed_data)
except ValueError as e:
    print(e)
