from random import randint


def threedsix():
    """returns 3d6 for stat generation"""
    return randint(1, 6) + randint(1, 6) + randint(1, 6)


ability_modifiers = {
    k: v
    for k, v in zip(
        range(3, 19), [-3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
    )
}

hit_die = {
    "Guerrier": 12,
    "Clerc": 8,
    "Voleur": 6,
    "Mage": 4,
    "Nain": 10,
    "Elfe": 6,
    "Halfelin": 6,
}
