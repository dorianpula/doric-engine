import random

Terrains = {
    'plain': {
        'color': '#71CD00'
    },
    'hill': {
        'color': '#505355'
    },
    'water': {
        'color': '#5D88F8'
    },
    'sand': {
        'color': '#F9CF29'
    },
    'forest': {
        'color': '#10A71E'
    },
    'city': {
        'color': '#A1A5AA'
    }
}


def choose_random_terrain():
    random_terrain_seed = random.randint(0, 100)
    terrain = 'plain'
    if 0 < random_terrain_seed < 20:
        terrain = 'forest'
    elif 20 < random_terrain_seed < 25:
        terrain = 'hill'
    elif 50 < random_terrain_seed < 60:
        terrain = 'water'
    elif 70 < random_terrain_seed < 90:
        terrain = 'sand'
    elif 90 < random_terrain_seed < 100:
        terrain = 'city'
    return terrain
