from requests import post
import json

with open("../schemas/habits_load_schema.json", mode="r") as schema:
    payload = json.load(schema)
    response = post("https://luscherian.herokuapp.com/beta_habits", json=payload).json()
    print(response)
