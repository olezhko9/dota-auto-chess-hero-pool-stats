from dota_auto_chess.hero_list import all_heroes
from .plot import *

heroes_stat = {}
classes_stat = {}
species_stat = {}


def update_heroes_stat(heroes):
    for hero in heroes:
        if heroes_stat.get(hero) is None:
            heroes_stat[hero] = 1
        else:
            heroes_stat[hero] += 1

        for species in all_heroes[hero].get("species"):
            if species_stat.get(species) is None:
                species_stat[species] = 1
            else:
                species_stat[species] += 1

        hero_class = all_heroes[hero].get("class")
        if classes_stat.get(hero_class) is None:
            classes_stat[hero_class] = 1
        else:
            classes_stat[hero_class] += 1

    return heroes_stat, classes_stat, species_stat
