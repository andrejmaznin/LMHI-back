from requests import post
import os

files = ["red", "green", "blue", "yellow", "main"]

for i in files:
    filename = i + ".txt"
    body = {"payload": [], "num": 0}
    with open(os.path.abspath(filename), encoding="utf-8") as f:
        lines = f.readlines()
        body["num"] = len(lines)
        for j in lines:
            code, info = j.rstrip("\n").split("  ")
            body["payload"].append({"code": i + "/" + code, "info": info})
        print(post("https://luscherian.herokuapp.com/result/multiple", json=body).json())
