#!/usr/bin/python

import json
import itertools

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
    "Smithing",
    "",
    "CURRENT_ITEM",
    "99",
    [["Start Skill", "Smithing", "NEXT_ITEM", "", ""]],
]

item_tuples = itertools.product(materials, items)
itemlist = []
for item in item_tuples:
    itemlist.append(item[0] + " " + item[1])

mastery_list = []
# Iterate through each pair
for grouping in itertools.pairwise(itemlist):
    mastery_list.append(
        [
            "Mastery Level",
            "Smithing",
            "",
            grouping[0],
            "99",
            [["Start Skill", "Smithing", grouping[1], "", ""]],
        ]
    )

# Manually add the final one
mastery_list.append(
    [
        "Mastery Level",
        "Smithing",
        "",
        itemlist[-1:][0],
        "99",
        [["Start Skill", "Agility", "", "", ""]],
    ]
)

with open("smithing_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
