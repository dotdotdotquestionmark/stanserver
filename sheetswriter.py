# write to sheet database, dont use pandas since it's single line ops
from __future__ import print_function
import json

from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from datetime import date

# @stanleywang do not feel dank about how this is written because 
# this entire shit ass concept is dank to begin with

# global spreadsheet details
GOOGLE_SHEETS_ID = "1lU1dA_JBxe4iRcd8LhCR3heKsipGcDziWwD_al7MD9k"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDENTIAL_FILE = "Credentials/contactformkeys.json" 
WORKSHEET_NAME = "inquiries!" #presence of the exclamation mark is terribly important in this scenario 

# Set up for linking up, grab credentials
account_credentials = service_account.Credentials.from_service_account_file(
    CREDENTIAL_FILE, scopes=SCOPES
    )
service_sheets = build('sheets', 'v4', credentials=account_credentials)

def datacollector():
    # gather data from where you wanna find it
    f = open('incoming.txt', 'r')
    temp = f.readline()
    client_data = json.loads(temp)
    f.close()

    client_name = client_data["name"]
    client_email = client_data["email"]
    client_phone = client_data["phone"]
    message = client_data["message"]
    entry_date = str(date.today())

    # create a dict to store the parsed data  
    input_values_list = [[client_name, client_email, client_phone, message, entry_date]]
    global input_values
    input_values = {
        'values' : input_values_list
    }
    print(input_values)

def locator():
    print("this is so stupid lmao")
    # loop through cells until blank is given 
    global write_range
    row_count = 2
    # while loop until first blank row is uncovered 
    while True:
        cell_value = service_sheets.spreadsheets().values().get(
            spreadsheetId=GOOGLE_SHEETS_ID,
            valueRenderOption='FORMATTED_VALUE',
            range=WORKSHEET_NAME+"A"+str(row_count)
        ).execute()
        print(cell_value)
        if "values" in cell_value:
            row_count += 1
        else:
            write_range = f"A{row_count}:E{row_count}"
            print(write_range)
            break
            

def courier():
    # lets try this
    service_sheets.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEETS_ID,
        valueInputOption='USER_ENTERED', 
        range=WORKSHEET_NAME + write_range,
        body=input_values
    ).execute()

def main():
    print("python script successfully running")
    datacollector()
    locator()
    courier()

if __name__ == "__main__":
    main()