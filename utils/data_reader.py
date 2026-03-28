import json

def get_test_data():
    with open("test_data/data.json") as f:
        return json.load(f)
