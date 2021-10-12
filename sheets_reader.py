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
    "Summoning": {"headers": "I4:I23", "values": "AL4:AL23"},
}

global_resource_count = dict()


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


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = generate_creds()
    # Get the values
    for skill in resource_map:
        print(f"***{skill.upper()}")
        headers = get_range_from_sheet(
            creds, f"{skill}!{resource_map[skill]['headers']}"
        )
        values = get_range_from_sheet(creds, f"{skill}!{resource_map[skill]['values']}")

        if not headers or not values:
            print("No data found.")
        else:
            print("Type, Count:")
            for h_row, v_row in zip(headers, values):
                # Strip out the commas and replace the empty cells with 0
                resource = str(h_row[0])
                count = int(
                    v_row[0]
                    .replace("Don't craft - use pool.", "0") # for Summoning
                    .replace("Craft for mastery pool XP.", "0") # for Summoning
                    .replace(",", "")
                    .replace("-", "0")
                )
                if resource not in global_resource_count:
                    global_resource_count[resource] = 0
                global_resource_count[resource] += count
                print(f"{resource}: {count}")

    # Write global resource count to disk
    with open("resources.json", "w") as f:
        json.dump(global_resource_count, f, indent=2)


if __name__ == "__main__":
    main()
# [END sheets_quickstart]
