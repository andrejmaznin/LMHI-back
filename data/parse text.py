from requests import post

filenames = ["yellow"]
for i in filenames:
    with open(i + ".txt", encoding="utf-8") as file:
        for line in file:
            line = line.split("  ")
            print(line)
            print(post("https://luscherian.herokuapp.com/result", json={"code": i + line[0], "info": line[1]}).json())
    