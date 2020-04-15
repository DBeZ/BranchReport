import pandas as pd
import gspread  # conda install -c conda-forge gspread
from df2gspread import df2gspread as d2g  # conda install -c conda-forge df2gspread
# from google import Create_Service #conda install -c conda-forge google-api-python-client
from oauth2client import service_account  # conda install -c conda-forge oauth2client
import pandas as pd
import numpy as np


def export_to_google_sheets(dataframe):
    jsonFile = 'doreen_shecodes_secret.json'  # Name of file downloaded when API is enabled on drive
    scope = ['https://www.googleapis.com/auth/spreadsheets',  # https://www.googleapis.com/auth/spreadsheets
             'https://www.googleapis.com/auth/drive.file']
    credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
        jsonFile, scope)  # load credentials from json file
    gc = gspread.authorize(credentials)
    spreadsheet_key = "1x4o8M1T8UlCOlwHxhRvkIk1qzuPREN5oD3LEbLXc_W0"  # spreadsheet id from sheet URL between '/d/' and '/edit#gid'
    wks_name = 'Attendance Report'  # sheet name
    d2g.upload(dataframe, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    print("Export to google sheets complete")
