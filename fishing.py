#!/usr/bin/env python310

import json
import itertools

SKILL = "Fishing"

# Standard Runes
raw_fish = [
    "Shrimp",
    "Lobster",
    "Crab",
    "Sardine",
    "Herring",
    "Carp",
    "Blowfish",
    "Poison Fish",
    "Anglerfish",
    "Cave Fish",
    "Trout",
    "Salmon",
    "Fanfish",
    "Swordfish",
    "Manta Ray",
    "Shark",
    "Whale",
    "Seahorse",
    "Skeleton Fish",
    "Magic Fish",
]

leaping_fish = [
    "Leaping Trout",
    "Salmon",
    "Broad Fish",
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
itemlist.extend(["Raw " + x for x in raw_fish])
itemlist.extend(["Leaping " + x for x in leaping_fish])

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
