#!/usr/bin/env python310

import json
import itertools

SKILL = "Agility"

agility_map = {
    "Cargo Net": 1,
    "Rope Swing": 1,
    "Rope Climb": 1,
    "Rope Jump": 2,
    "Monkey Bars": 2,
    "Balance Beam": 2,
    "Balance Seesaw": 3,
    "Pipe Climb": 3,
    "Pipe Balance": 3,
    "Pit Jump": 3,
    "Stepping Stones": 3,
    "Burning Coals": 3,
    "Coal Stones": 4,
    "Mud Crawl": 4,
    "Mud Dive": 4,
    "Cave Climb": 4,
    "Gap Jump": 4,
    "Rock Climb": 5,
    "Cliff Climb": 5,
    "Cliff Balance": 5,
    "Mountain Climb": 5,
    "Tree Climb": 5,
    "Rooftop Run": 5,
    "Tree Hop": 6,
    "Tree Balance": 6,
    "Rocky Waters": 6,
    "Lake Swim": 6,
    "Raft Drifting": 6,
    "Forest Trail": 6,
    "Spike Trap": 7,
    "Heat Trap": 7,
    "Boulder Trap": 7,
    "Water Trap": 7,
    "Freezing Trap": 7,
    "Pipe Crawl": 8,
    "Raft Building": 8,
    "Spike Jump": 8,
    "Tree Hang": 8,
    "A Lovely Jog": 8,
    "Runic Trail": 8,
    "Sweltering Pools": 8,
    "Lava Jump": 9,
    "Water Jump": 9,
    "Ice Jump": 9,
    "Cave Maze": 9,
    "Frozen Lake Crossing": 9,
    "Waterfall": 10,
    "Lava Waterfall Dodge": 10,
    "Boulder Move": 10,
    "Dragon Fight": 10,
    "Ocean Rafting": 10,
}

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
                [
                    ["Build Agility Obstacle", str(agility_map[grouping[1]]), grouping[1], "", ""],
                    ["Start Skill", SKILL, "", "", ""],
                ],
            ]
        )
    return mastery_list


mastery_list = []
itemlist = []
itemlist.extend(itertools.chain(agility_map))

# Manually add the starting point
mastery_list.append(
    [
        "Idle",
        "",
        "",
        "",
        "",
        [
            ["Build Agility Obstacle", "1", itemlist[0], "", ""],
            ["Start Skill", SKILL, "", "", ""],
        ],
    ],
)

# Generate the rest of the lists
mastery_list.extend(generate_list(itemlist))

with open(f"{SKILL.lower()}_mastery.txt", "w") as f:
    json.dump(mastery_list, f, sort_keys=False, indent=2)
