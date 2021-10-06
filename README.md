# Melvor Action Queue 99 Mastery Scripts

These scripts will generate action queues to be used with [Melvor Action Queue](https://greasyfork.org/en/scripts/412689-melvor-action-queue).

Each skill script (such as "crafting.py"), when run, will generate a text file that can be copy-pasted into the Melvor Action Queue "Import Action List" field. For convenience, the output of those scripts are already included in the repo.

As of 10/5/2021, this is compatible with Melvor Idle 0.22.

## How to use the Action Queues
1. Open the txt file for the skill you want to master
2. Copy the (JSON-formatted) contents
3. Paste into Melvor Action Queue's "Paste data here" field
4. You likely want to be idle when you start, and with an already paused queue
5. Unpause the action queue and let it go to work

## What These Action Queues Do
These are intended for grinding to 99 mastery in each skill. Assuming you are starting idle, it will begin the first item in a skill. Once you have reached 99 mastery of that item, it will proceed to the next one - and so on, and so forth. Because it does a 99 mastery check, this can easily accommodate any existing state of mastery - it'll just skip over ones you've already mastered.

**Important Note:** This does _not_ do any materials check. It naively assumes you already have all the materials necessary to complete the mastery. If you run out of materials, the queue will simply stop and get stuck. It's up to you to calculate the necessary amount of materials to stock up on in order to complete the mastery requirement. I recommend checking out existing spreadsheets or other extensions/scripts/simulators to help calculate how much you need.

## Dependencies
You need [Melvor Action Queue](https://greasyfork.org/en/scripts/412689-melvor-action-queue) to actually use the contents in the .txt files. As of 10/5/2021, you need version 0.7.0 installed (although it will probably work on earlier versions, it is untested).

To run the scripts themselves, you need Python 3.10 (the first version of Python to include itertools.pairwise).

## How to Generate New Mastery Queues
Using Python 3.10 on any platform, simply execute each of the skill python files you want:

  python3.exe smithing.py
  /usr/local/bin/python3 smithing.py
