import json

def get_test_data():
    with open("data.json") as f:
        return json.load(f)
