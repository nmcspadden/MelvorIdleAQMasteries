#!/usr/bin/python

import json
import itertools

SKILL = "Smithing"

items = [
    "Dagger",
    "Throwing Knife",
    "Sword",
    "Arrowtips",
    "Gloves",
    "Scimitar",
    "Helmet",
    "Battleaxe",
    "Javelin Heads",
    "Boots",
    "Shield",
    "2H Sword",
    "Crossbow Head",
    "Platelegs",
    "Platebody",
]

materials = ["Bronze", "Iron", "Steel", "Mithril", "Adamant", "Rune", "Dragon"]

mastery_item = [
    "Mastery Level",
    SKILL,
    "",
    "CURRENT_ITEM",
    "99",
    [["Start Skill", SKILL, "NEXT_ITEM", "", ""]],
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
                SKILL,
                "",
                grouping[0],
                "99",
                [["Start Skill", SKILL, grouping[1], "", ""]],
            ]
        )
    return mastery_list


mastery_list = []
itemlist = []
itemlist.extend(itemize(materials, items))

# Manually add the starting point
mastery_list.append(
    ["Idle", "", "", "", "", [["Start Skill", SKILL, itemlist[0], "", ""]]]
)

# Generate the rest of the lists
mastery_list.extend(generate_list(itemlist))

# Manually add the final one
mastery_list.append(
    [
        "Mastery Level",
        SKILL,
        "",
        itemlist[-1:][0],
        "99",
        [["Start Skill", "Agility", "", "", ""]],
    ]
)

with open("smithing_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
