
import gspread  # conda install -c conda-forge gspread
from df2gspread import df2gspread as d2g  # conda install -c conda-forge df2gspread
from oauth2client import service_account  # conda install -c conda-forge oauth2client
from datetime import datetime

import os


def export_to_google_sheets(dataframe):
    working_folder = os.getcwd()
    try:
        os.chdir(str("User_specific_files"))
        jsonFile = 'API_login.json'  # Name of file downloaded when API is enabled on drive
        scope = ['https://www.googleapis.com/auth/spreadsheets',  # https://www.googleapis.com/auth/spreadsheets
                 'https://www.googleapis.com/auth/drive.file']
        credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
            jsonFile, scope)  # load credentials from json file
        gc = gspread.authorize(credentials)
        os.chdir("..")
        spreadsheet_key = "1x4o8M1T8UlCOlwHxhRvkIk1qzuPREN5oD3LEbLXc_W0"  # spreadsheet id from sheet URL between '/d/' and '/edit#gid'
        wks_name = 'Attendance Report'  # sheet name
        d2g.upload(dataframe, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
        print("Export to google sheets complete")
    except:
        print("Export to google sheets failed")
        print("Report will be saved instead")
        os.chdir(working_folder)
        export_to_csv(dataframe, "WeeklyReport")


def export_to_csv(dataframe, report_name):
    now = str(datetime.now().strftime("%y%m%d %H_%M"))
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    dataframe.to_csv(os.getcwd() + "\\" + report_name + now + ".csv", index=True, header=True)
    os.chdir("..")
    print("Results saved as csv")
