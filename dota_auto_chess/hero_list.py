import os
import json

data_file_path = os.path.join(os.path.dirname(__file__), 'data/heroes.json')
with open(data_file_path) as heroes_data:
    all_heroes = json.loads(heroes_data.read())

print(all_heroes)
