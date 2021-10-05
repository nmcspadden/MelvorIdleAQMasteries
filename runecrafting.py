#!/usr/local/bin/fbpython

import json
import itertools

staves_of = [
    "Staff of",
]

battlestaves = [
    "Battlestaff",
]

mystic_staves = [
    "Mystic",
]

wands = [
    "Imbued Wand",
]

elements = [
    "Air",
    "Water",
    "Earth",
    "Fire",
]

staff = [
    "Staff"
]

mastery_item = [
    "Mastery Level",
    "Crafting",
    "",
    "CURRENT_ITEM",
    "99",
    [
        [
            "Start Skill",
            "Crafting",
            "NEXT_ITEM",
            "",
            ""
        ]
    ]
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
                "Runecrafting",
                "",
                grouping[0],
                "99",
                [
                    [
                        "Start Skill",
                        "Runecrafting",
                        grouping[1],
                        "",
                        ""
                    ]
                ]
            ]    
        )
    return mastery_list

mastery_list = []
itemlist = []
itemlist.extend(itemize(staves_of, elements))
itemlist.extend(itemize(elements, battlestaves))
itemlist.extend(itemize(mystic_staves, elements, staff))
itemlist.extend(itemize(elements, wands))
mastery_list.extend(generate_list(itemlist))

with open("runecrafting_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)