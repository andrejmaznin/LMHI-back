from requests import post
import json

with open("../schemas/mood_criterias_load_schema.json", mode="r") as schema:
    payload = json.load(schema)
    response = post("https://luscherian.herokuapp.com/mood_criteria", json=payload).json()
    print(response)
