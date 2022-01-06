import json

from requests import post

with open("../service_schemas/load_mood_criterias.json", mode="r") as schema:
    payload = json.load(schema)
    response = post("https://luscherian.herokuapp.com/mood_criteria", json=payload).json()
    print(response)
