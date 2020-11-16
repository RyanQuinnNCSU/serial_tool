import json


# with open("../json/profile1.json", "r") as read_file:
#     data = json.loads(read_file.read())
#     print(data)
data = {}

with open("../json/config.json", "r") as read_file:
    data = json.loads(read_file.read())
    print(data['COM List'])
data['COM List'] = []
data['COM List'].append("COM11")
data['COM List'].append("COM14")
print(data['COM List'])
with open("../json/config.json", "w") as write_file:
    json.dump(data, write_file)
