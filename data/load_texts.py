from requests import post

files = ["red.txt", "green.txt", "blue.txt", "yellow.txt", "main.txt"]

for i in files:
    with open(i, encoding="utf-8") as f:
        for j in f.readlines():
            code, info = j.rstrip("\n").split("  ")
            d = {"code": i + "/" + code, "info": info}
            print(post("https://luscherian.herokuapp.com/result", json=d).json())

