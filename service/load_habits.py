import json

from requests import post

with open("../service_schemas/load_habits.json", mode="r") as schema:
    payload = json.load(schema)
    response = post("http://localhost:8080/beta_habits", json=payload).json()
    print(response)
