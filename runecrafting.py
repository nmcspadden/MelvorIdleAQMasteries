#!/usr/bin/env python310

import json
import itertools

# Standard Runes
standard_elements = [
    "Air",
    "Mind",
    "Water",
    "Earth",
    "Fire",
    "Light",
    "Body",
    "Chaos",
    "Nature",
    "Havoc",
    "Death",
    "Blood",
    "Spirit",
    "Ancient",
]

# Combination Runes
combo_elements = [
    "Mist",
    "Dust",
    "Mud",
    "Smoke",
    "Steam",
    "Lava",
]

# Staves & Wands
staff_elements = [
    "Air",
    "Water",
    "Earth",
    "Fire",
]

# Magic Gear
gear_levels = ["Acolyte", "Adept", "Expert"]

gear_types = ["Wizard Hat", "Wizard Boots", "Wizard Bottoms", "Wizard Robes"]

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
                "Runecrafting",
                "",
                grouping[0],
                "99",
                [["Start Skill", "Runecrafting", grouping[1], "", ""]],
            ]
        )
    return mastery_list


mastery_list = []
itemlist = []
itemlist.extend(itemize(standard_elements, ["Rune"]))
itemlist.extend(itemize(combo_elements, ["Rune"]))
itemlist.extend(itemize(["Staff of"], staff_elements))
itemlist.extend(itemize(staff_elements, ["Battlestaff"]))
itemlist.extend(itemize(["Mystic"], staff_elements, ["Staff"]))
itemlist.extend(itemize(staff_elements, ["Imbued Wand"]))
itemlist.extend(itemize(staff_elements, gear_levels, gear_types))

# Manually add the starting point
mastery_list.append(
    ["Idle", "", "", "", "", [["Start Skill", "Runecrafting", itemlist[0], "", ""]]]
)

# Generate the rest of the lists
mastery_list.extend(generate_list(itemlist))

# Manually add the final agility
mastery_list.append(
    [
        "Mastery Level",
        "Runecrafting",
        "",
        itemlist[-1],
        "99",
        [["Start Skill", "Agility", "", "", ""]],
    ]
)

with open("runecrafting_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
