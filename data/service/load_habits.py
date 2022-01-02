from requests import post
import json

with open("../schemas/load_habits.json", mode="r") as schema:
    payload = json.load(schema)
    response = post("https://luscherian.herokuapp.com/beta_habits", json=payload).json()
    print(response)
