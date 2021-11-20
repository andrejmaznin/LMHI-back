from requests import post

files = ["red.txt", "green.txt", "blue.txt", "yellow.txt", "main.txt"]

for i in files:
    with open(i, encoding="utf-8") as f:
        for j in f.readlines():
            code, info = j.rstrip("\n").split("  ")
            d = {"code": code, "info": info}
            print(post("http://127.0.0.1:8000/result", json=d).json())
