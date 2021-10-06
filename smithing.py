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

item_tuples = itertools.product(materials, items)
itemlist = []
for item in item_tuples:
    itemlist.append(item[0] + " " + item[1])

mastery_list = []

# Manually add the starting point
mastery_list.append(
    ["Idle", "", "", "", "", [["Start Skill", SKILL, itemlist[0], "", ""]]]
)

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
