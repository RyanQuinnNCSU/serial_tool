import json


with open("../json/profile1.json", "r") as read_file:
    data = json.loads(read_file.read())
    print(data)
