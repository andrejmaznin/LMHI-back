from requests import post
with open("blue.txt", encoding="utf-8") as file:
    for line in file:
        line = line.split("  ")
        print(line)
        print(post("http://localhost:8080/result", json={"code": "blue" + line[0], "info": line[1]}).json())