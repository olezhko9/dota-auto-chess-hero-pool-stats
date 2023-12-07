import json

with open('./heroes.json') as heroes_data:
    all_heroes = json.loads(heroes_data.read())

print(all_heroes)
