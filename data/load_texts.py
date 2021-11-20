from requests import post

files = ["red", "green", "blue", "yellow", "main"]

for i in files:
    filename = i + ".txt"
    with open(filename, encoding="utf-8") as f:
        for j in f.readlines():
            code, info = j.rstrip("\n").split("  ")
            d = {"code": i + "/" + code, "info": info}
            print(post("https://luscherian.herokuapp.com/result", json=d).json())
