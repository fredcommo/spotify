import json

creds_file = ".credentials.json"
with open(creds_file) as json_file:
    creds = json.load(json_file)

print(creds)