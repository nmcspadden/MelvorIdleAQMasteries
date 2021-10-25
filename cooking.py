#!/usr/bin/env python310

import json
import itertools

SKILL = "Cooking"

recipes = [
    "Shrimp",
    "Beef",
    "Sardine",
    "Herring",
    "Seahorse",
    "Trout",
    "Salmon",
    "Lobster",
    "Swordfish",
    "Anglerfish",
    "Fanfish",
    "Crab",
    "Carp",
    "Shark",
    "Cave Fish",
    "Manta Ray",
    "Whale",
    "Bread",
    "Chicken",
    "Plain Pizza Slice",
    "Beef Pie",
    "Meat Pizza Slice",
    "Strawberry Cupcake",
    "Cherry Cupcake",
    "Apple Pie",
    "Strawberry Cake",
    "Carrot Cake",
    "Basic Soup",
    "Hearty Soup",
    "Cream Corn Soup",
    "Chicken Soup"
]

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
itemlist.extend(recipes)

# Manually add the starting point
mastery_list.append(
    ["Idle", "", "", "", "", [["Start Skill", SKILL, itemlist[0], "", ""]]]
)

# Generate the rest of the lists
mastery_list.extend(generate_list(itemlist))

# Manually add the final agility
mastery_list.append(
    [
        "Mastery Level",
        SKILL,
        "",
        itemlist[-1],
        "99",
        [["Start Skill", "Agility", "", "", ""]],
    ]
)

with open(f"{SKILL.lower()}_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
