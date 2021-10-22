# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import itertools

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
MELVOR_RATES_RESOURCES_COPY = "1s4dhrUKTgGZ_nVe_x0bR3Olmcwijp_ta9kZmTVzZDVo"
SAMPLE_RANGE_NAME = "Runecrafting!AH4:AI20"

resource_map = {
    "Runecrafting": {"headers": "AH4:AH20", "values": "AI4:AI20"},
    "Crafting": {"headers": "AG4:AG19", "values": "AF4:AF19"},
    "Fletching": {"headers": "AI4:AI58", "values": "AH4:AH58"},
    "Smithing": {"headers": "AI4:AI20", "values": "AJ4:AJ20"},
    "Cooking": {"headers": "H4:H34", "values": "AI4:AI34"},
    "Herblore": {
        "headers": "AK4:AK28",
        "values": "AL4:AF28",
    },  # this one has a "next page" option...
    "Summoning": {
        "headers": "Summoning_Name",
        "values": "AL4:AL23",
    },  # the resources here are combined in the values
    "Firemaking": {"headers": "Firemaking_Name", "values": "W5:W13"},
}

gathering_map = {
    "Woodcutting": "Woodcutting_Name",
    "Fishing": "Fishing_Name",
    "Mining": "Mining_Name",
    "Thieving": "Thieving_Name",
    "Farming": "Farming_Name", # this one has some header rows that have no values?
    "Agility": "Agility_Name",
}

cooking_map = {
    "headers": "Cooking_Name",
    "ingredient_1": "Cooking_Ingredient1",
    "ingredient_2": "Cooking_Ingredient2",
    "ingredient_3": "Cooking_Ingredient3",
    "ingredient_4": "Cooking_Ingredient4",
    "ingredientamt_1": "Cooking_IngredientAmount1",
    "ingredientamt_2": "Cooking_IngredientAmount2",
    "ingredientamt_3": "Cooking_IngredientAmount3",
    "ingredientamt_4": "Cooking_IngredientAmount4",
    "mastery_resources": "AI4:AI34",
}

herblore_map = {
    "headers": "Herblore_Name",
    "ingredient_1": "Herblore_Ingredient1",
    "ingredient_2": "Herblore_Ingredient2",
    "ingredient_3": "Herblore_Ingredient3",
    "ingredientamt_1": "Herblore_IngredientAmount1",
    "ingredientamt_2": "Herblore_IngredientAmount2",
    "ingredientamt_3": "Herblore_IngredientAmount3",
    "mastery_resources": "AG4:AG29",
}

global_resource_count = {"Global": {}}


def generate_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_range_from_sheet(creds, range_string):
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=MELVOR_RATES_RESOURCES_COPY, range=range_string)
        .execute()
    )
    return result.get("values", [])


def get_cooking(creds):
    """Cooking ingredients are also combined"""
    skill = "Cooking"
    global_resource_count[skill] = {}
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .batchGet(
            spreadsheetId=MELVOR_RATES_RESOURCES_COPY,
            ranges=[
                f"{skill}!{cooking_map['headers']}",
                f"{skill}!{cooking_map['ingredient_1']}",
                f"{skill}!{cooking_map['ingredientamt_1']}",
                f"{skill}!{cooking_map['ingredient_2']}",
                f"{skill}!{cooking_map['ingredientamt_2']}",
                f"{skill}!{cooking_map['ingredient_3']}",
                f"{skill}!{cooking_map['ingredientamt_3']}",
                f"{skill}!{cooking_map['ingredient_4']}",
                f"{skill}!{cooking_map['ingredientamt_4']}",
                f"{skill}!{cooking_map['mastery_resources']}",
            ],
        )
        .execute()
    )
    values = result.get("valueRanges", [])
    headers = itertools.chain.from_iterable(values[0]["values"])
    ingredients_1 = itertools.chain.from_iterable(values[1]["values"])
    ingredientsamts_1 = itertools.chain.from_iterable(values[2]["values"])
    ingredients_2 = itertools.chain.from_iterable(values[3]["values"])
    ingredientsamts_2 = itertools.chain.from_iterable(values[4]["values"])
    ingredients_3 = itertools.chain.from_iterable(values[5]["values"])
    ingredientsamts_3 = itertools.chain.from_iterable(values[6]["values"])
    ingredients_4 = itertools.chain.from_iterable(values[7]["values"])
    ingredientsamts_4 = itertools.chain.from_iterable(values[8]["values"])
    counts = itertools.chain.from_iterable(values[9]["values"])
    for potion, ing1, ingamt1, ing2, ingamt2, ing3, ingamt3, ing4, ingamt4, count in zip(
        headers,
        ingredients_1,
        ingredientsamts_1,
        ingredients_2,
        ingredientsamts_2,
        ingredients_3,
        ingredientsamts_3,
        ingredients_4,
        ingredientsamts_4,
        counts,
    ):
        # print(f"Potion: {potion}")
        # First ingredient
        actual_amount_1 = calculate_ingredients(skill, ing1, ingamt1, count)
        if actual_amount_1 > 0:
            print(f"{ing1}: {actual_amount_1}")
        # Second ingredient
        if ing2 == "-":
            # if there's only one ingredient, next potion
            # there is never a case where this no second ingredient but is a third
            continue
        actual_amount_2 = calculate_ingredients(skill, ing2, ingamt2, count)
        if actual_amount_2 > 0:
            print(f"{ing2}: {actual_amount_2}")
        # Third ingredient
        if ing3 == "-":
            continue
        actual_amount_3 = calculate_ingredients(skill, ing3, ingamt3, count)
        if actual_amount_3 > 0:
            print(f"{ing3}: {actual_amount_3}")
        # Fourth ingredient
        if ing4 == "-":
            continue
        actual_amount_4 = calculate_ingredients(skill, ing4, ingamt4, count)
        if actual_amount_4 > 0:
            print(f"{ing3}: {actual_amount_3}")


def calculate_ingredients(skill, ingredient, amount, count):
    """Calculate the number of ingredients required for 99 mastery"""
    fixed_count = int(count.replace(",", "").replace("-", "0"))
    if fixed_count == 0 or int(amount) == 0:
        return 0
    actual_amount = int(fixed_count) * int(amount)
    if ingredient not in global_resource_count[skill]:
        global_resource_count[skill][ingredient] = 0
    # Actual resource cost is "ingamt" * mastery count to get to 99
    global_resource_count[skill][ingredient] += actual_amount
    # Add to global skill group
    if ingredient not in global_resource_count["Global"]:
        global_resource_count["Global"][ingredient] = 0
    global_resource_count["Global"][ingredient] += actual_amount
    return actual_amount


def get_herblore(creds):
    """Herblore is a special case because each item has two ingredients."""
    skill = "Herblore"
    global_resource_count[skill] = {}
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .batchGet(
            spreadsheetId=MELVOR_RATES_RESOURCES_COPY,
            ranges=[
                f"{skill}!{herblore_map['headers']}",
                f"{skill}!{herblore_map['ingredient_1']}",
                f"{skill}!{herblore_map['ingredientamt_1']}",
                f"{skill}!{herblore_map['ingredient_2']}",
                f"{skill}!{herblore_map['ingredientamt_2']}",
                f"{skill}!{herblore_map['ingredient_3']}",
                f"{skill}!{herblore_map['ingredientamt_3']}",
                f"{skill}!{herblore_map['mastery_resources']}",
            ],
        )
        .execute()
    )
    values = result.get("valueRanges", [])
    headers = itertools.chain.from_iterable(values[0]["values"])
    ingredients_1 = itertools.chain.from_iterable(values[1]["values"])
    ingredientsamts_1 = itertools.chain.from_iterable(values[2]["values"])
    ingredients_2 = itertools.chain.from_iterable(values[3]["values"])
    ingredientsamts_2 = itertools.chain.from_iterable(values[4]["values"])
    ingredients_3 = itertools.chain.from_iterable(values[5]["values"])
    ingredientsamts_3 = itertools.chain.from_iterable(values[6]["values"])
    counts = itertools.chain.from_iterable(values[7]["values"])
    for potion, ing1, ingamt1, ing2, ingamt2, ing3, ingamt3, count in zip(
        headers,
        ingredients_1,
        ingredientsamts_1,
        ingredients_2,
        ingredientsamts_2,
        ingredients_3,
        ingredientsamts_3,
        counts,
    ):
        # print(f"Potion: {potion}")
        # First ingredient
        actual_amount_1 = calculate_ingredients(skill, ing1, ingamt1, count)
        if actual_amount_1 > 0:
            print(f"{ing1}: {actual_amount_1}")
        # Second ingredient
        if ing2 == "-":
            # if there's only one ingredient, next potion
            # there is never a case where this no second ingredient but is a third
            continue
        actual_amount_2 = calculate_ingredients(skill, ing2, ingamt2, count)
        if actual_amount_2 > 0:
            print(f"{ing2}: {actual_amount_2}")
        # Third ingredient
        if ing3 == "-":
            continue
        actual_amount_3 = calculate_ingredients(skill, ing3, ingamt3, count)
        if actual_amount_3 > 0:
            print(f"{ing3}: {actual_amount_3}")


def get_summoning(values):
    """Summoning requires parsing out the results from a single column"""
    skill = "Summoning"
    for v_row in values:
        if v_row[0] == "-" or "Don't craft" in v_row[0] or "Craft for" in v_row[0]:
            continue
        first_pass_values = v_row[0].split(", and ")
        # ['60,056 Dragon Bones', '108,100 Red, 84,078 Blue, 60,055 Gold Shards']
        shards = first_pass_values[1].split(", ")
        # ['108,100 Red', '84,078 Blue', '60,055 Gold Shards']
        shardmap = {
            "Red Shards": 0,
            "Green Shards": 0,
            "Blue Shards": 0,
            "Silver Shards": 0,
            "Gold Shards": 0,
            "Black Shards": 0,
        }
        reslist = []
        # Strip out the commas and replace the empty cells with 0
        resource_name = first_pass_values[0].split(" ", 1)[1]
        resource_count = int(
            first_pass_values[0].split(" ", 1)[0].replace(",", "").replace("-", "0")
        )
        reslist.append((resource_name, resource_count))
        print(f"{resource_name}: {resource_count}")
        for color in shards:
            shard_split = color.split(" ")
            count = int(shard_split[0].replace(",", ""))
            shard = shard_split[1]
            if " Shards" not in shard:
                shard += " Shards"
            shardmap[shard] += int(count)
            reslist.append((shard, count))
        for resource, count in reslist:
            # Add to individual skill key
            if resource not in global_resource_count[skill]:
                global_resource_count[skill][resource] = 0
            global_resource_count[skill][resource] += count
            # Add to global skill group
            if count == 0:
                # Don't bother adding 0s to the global count
                continue
            if resource not in global_resource_count["Global"]:
                global_resource_count["Global"][resource] = 0
            global_resource_count["Global"][resource] += count
            print(f"{resource}: {count}")


def get_skill(headers, values, skill):
    for h_row, v_row in zip(headers, values):
        # Strip out the commas and replace the empty cells with 0
        resource = str(h_row[0])
        count = int(
            v_row[0]
            .replace(",", "")
            .replace("-", "0")
        )
        # Add to individual skill key
        if resource not in global_resource_count[skill]:
            global_resource_count[skill][resource] = 0
        global_resource_count[skill][resource] += count
        # Add to global skill group
        if count == 0:
            # Don't bother adding 0s to the global count
            continue
        if resource not in global_resource_count["Global"]:
            global_resource_count["Global"][resource] = 0
        global_resource_count["Global"][resource] += count
        print(f"{resource}: {count}")


def main():
    """Use the Rate and Resources spreadsheet to calculate resources needed for 99 mastery"""
    creds = generate_creds()
    # Get the necessary ingredients for crafting
    for skill in resource_map:
        global_resource_count[skill] = {}
        print(f"***{skill.upper()}")
        headers = get_range_from_sheet(
            creds, f"{skill}!{resource_map[skill]['headers']}"
        )
        values = get_range_from_sheet(creds, f"{skill}!{resource_map[skill]['values']}")

        if not headers or not values:
            print("No data found.")
        elif skill == "Summoning":
            # Summoning is a special case where the list of ingredients is combined on each row
            get_summoning(values)
        elif skill == "Herblore":
            # Herblore is a special case because there are multiple ingredients required per item
            get_herblore(creds)
        elif skill == "Cooking":
            # Cooking also has multipe ingredients
            get_cooking(creds)
        else:
            get_skill(headers, values, skill)

    # Write global resource count to disk
    with open("resources.json", "w") as f:
        json.dump(global_resource_count, f, indent=2)


if __name__ == "__main__":
    main()
