import json

from requests import post

BASE_URL = 'https://iluscherian.herokuapp.com'


def load_mood_criterias(base_path: str = ''):
    with open(base_path + '/service_schemas/load_mood_criterias.json', mode="r") as schema:
        payload = json.load(schema)
        response = post(BASE_URL + "/mood_criteria", json=payload).json()
        print(response)


def load_habits(base_path: str = ''):
    with open(base_path + "service_schemas/load_habits.json", mode="r") as schema:
        payload = json.load(schema)
        response = post(BASE_URL + "/habits", json=payload).json()
        print(response)


def load_interpretations(base_path: str = ''):
    with open(base_path + "/service_schemas/load_texts.json", mode="r") as schema:
        payload = json.load(schema)
        response = post(BASE_URL + "/result/multiple", json=payload).json()
        print(response)


def main(base_path: str = ''):
    load_mood_criterias(base_path)
    load_habits(base_path)
    load_interpretations(base_path)


if __name__ == "__main__":
    main('../')
