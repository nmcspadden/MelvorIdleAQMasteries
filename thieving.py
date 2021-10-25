#!/usr/bin/env python310

import json
import itertools

SKILL = "Thieving"

targets = [
    "Man",
    "Woman",
    "Golbin",
    "Golbin Chief",
    "Bandit Thug",
    "Marauder",
    "Merchant",
    "Bob the Farmer",
    "Assistant Cook",
    "Chef",
    "Dock Hand",
    "Fisherman",
    "Troll",
    "Cyclops",
    "Lumberjack",
    "Miner",
    "Squire",
    "Knight",
    "Acolyte",
    "Wizard",
    "Court Jester",
    "Princess",
    "King",
]

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
itemlist.extend(targets)

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
