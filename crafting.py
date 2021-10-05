#!/usr/bin/python

import json
import itertools

leather_items = [
    "Gloves",
    "Boots",
    "Cowl",
    "Vambraces",
    "Body",
    "Chaps",
]

leather_materials = ["Leather", "Hard Leather"]

dhide_items = ["Vambraces", "Chaps", "Shield", "Body"]

dhide_materials = ["Green D-hide", "Blue D-hide", "Red D-hide", "Black D-hide"]

jewels_items = ["Topaz", "Sapphire", "Ruby", "Emerald", "Diamond"]

jewelry_types = ["Ring", "Necklace"]

rings_materials = ["Silver", "Gold"]

mastery_item = [
    "Mastery Level",
    "Crafting",
    "",
    "CURRENT_ITEM",
    "99",
    [["Start Skill", "Crafting", "NEXT_ITEM", "", ""]],
]


def itemize(*args):
    if len(args) == 3:
        return [" ".join((x, y, z)) for (x, y, z) in itertools.product(*args)]
    return [" ".join((x, y)) for (x, y) in itertools.product(*args)]


def generate_list(itemlist):
    mastery_list = []
    # Iterate through each pair
    for grouping in itertools.pairwise(itemlist):
        mastery_list.append(
            [
                "Mastery Level",
                "Crafting",
                "",
                grouping[0],
                "99",
                [["Start Skill", "Crafting", grouping[1], "", ""]],
            ]
        )
    return mastery_list


mastery_list = []
itemlist = []
itemlist.extend(itemize(leather_materials, leather_items))
itemlist.extend(itemize(dhide_materials, dhide_items))
itemlist.extend(itemize(rings_materials, jewels_items, jewelry_types))
mastery_list.extend(generate_list(itemlist))

# Manually add the final one
mastery_list.append(
    [
        "Mastery Level",
        "Smithing",
        "",
        "Gold Diamond Necklace",
        "99",
        [["Start Skill", "Agility", "", "", ""]],
    ]
)

with open("crafting_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
