import gspread
from df2gspread import df2gspread as d2g
from oauth2client import service_account
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
import httplib2

import os


def export_to_google_sheets(dataframe, sheets_file_name, tab_name):
    spreadsheet_id = "1x4o8M1T8UlCOlwHxhRvkIk1qzuPREN5oD3LEbLXc_W0"  # spreadsheet id from sheet URL between '/d/' and '/edit#gid'

    working_folder = os.getcwd()
    try:
        os.chdir(str("User_specific_files"))
        jsonFile = 'API_login.json'  # Name of file downloaded when API is enabled on drive
        scope = ['https://www.googleapis.com/auth/spreadsheets']  # ,  'https://www.googleapis.com/auth/drive.file'
        credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
            jsonFile, scope)  # load credentials from json file
        gc = gspread.authorize(credentials)
        os.chdir("..")
        wks_name = tab_name
        d2g.upload(dataframe, spreadsheet_id, wks_name, credentials=credentials, row_names=True)
        print("Export to google sheets complete")
    except:
        print("Export to google sheets failed")
        print("Report will be saved instead")
        os.chdir(working_folder)
        export_to_csv(dataframe, sheets_file_name)


def export_to_csv(dataframe, report_name):
    now = str(datetime.now().strftime("%y%m%d %H_%M"))
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    dataframe.to_csv(os.getcwd() + "\\" + report_name + now + ".csv", index=True, header=True)
    os.chdir("..")
    print("Results saved as csv")


def export_figures_to_drive(figure_name):
    drive_folder_id = '11CLJVjytkcECd-7dGWKHAD-N0qD1RGST'
    file_name = figure_name + ".png"

    os.chdir("Output_files")
    output_dir = os.getcwd()
    os.chdir("..")

    try:
        g_login = GoogleAuth('drive_login.yaml')
        g_login.LocalWebserverAuth()
        drive = GoogleDrive(g_login)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == 'Weekly Report':
                folder_id = file.get('id')
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file1 in file_list:
            if file1['title'] == file_name:
                file1.Delete()
        os.chdir(output_dir)
        file_on_drive = drive.CreateFile({'parents': [{'id': drive_folder_id}]})
        file_on_drive.SetContentFile(file_name)
        file_on_drive.Upload()
    except:
        print("Error uploading file to drive")

    os.chdir("..")
    print('Graph Export to drive complete - %s' % (file_name))


'''
def insert_figure_image_to_sheet(image_file_name, sheets_file_name, tab_name):
    image_url="https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Fpenguin-images-free.html&psig=AOvVaw1_6tqfSRpyq7FcNqAveEpD&ust=1587332101390000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOi1g4L38ugCFQAAAAAdAAAAABAD"

    os.chdir(str("User_specific_files"))
    jsonFile = 'API_login.json'  # Name of file downloaded when API is enabled on drive
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
        jsonFile, scope)  # load credentials from json file
    gc = gspread.authorize(credentials)
    worksheets = gc.open(sheets_file_name).worksheets()
    for worksheet in worksheets:
        if worksheet.title =='Attendance Graphs':
            # worksheet.append_row([image_file_name, '=IMAGE(\"{}\")'.format(image_url)], 'USER_ENTERED')

            worksheet.append_row([image_file_name, '=IMAGE(\"{}\")'.format(image_url)])
    os.chdir("..")

    # TODO: insert figure into sheets
    pass

'''


def insert_figure_image_to_slides(figure_name, slides_file_name, page_id):
    presentation_id = "1obMYhzJdI8s9kDO4GOXr192NhtNxpMsFH51Lxy-9maw"  # spreadsheet id from sheet URL between '/d/' and '/edit#gid'

    working_folder = os.getcwd()

    os.chdir(str("User_specific_files"))
    jsonFile = 'API_login.json'  # Name of file downloaded when API is enabled on drive
    scope = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive.file']  #
    credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(jsonFile, scopes=scope
                                                                                   )
    # credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
    #     jsonFile, )  # load credentials from json file

    # flow = InstalledAppFlow.from_client_secrets_file(
    #     jsonFile, scope)
    # creds = flow.run_local_server(port=0)
    # service = build('slides', 'v1', credentials=creds)
    service = build('slides', 'v1', http=credentials.authorize(httplib2.Http()), cache_discovery=False)
    os.chdir("..")

    # page_id = add_slides(presentation_id, 1, 'BLANK')[0]
    # service.slides_service.presentations()

    slides = service.presentations().get(presentationId=presentation_id,
                                         fields='slides').execute().get('slides')
    page_ids = []
    for slide in slides:
        page_ids.append(slide['objectId'])

    IMAGE_URL = ('https://www.google.com/images/branding/'
                 'googlelogo/2x/googlelogo_color_272x92dp.png')
    requests = []
    image_id = 'MyImage_01'

    emu4M = {
        'magnitude': 4000000,
        'unit': 'EMU'
    }

    requests.append({
        'createImage': {
            'objectId': image_id,
            'elementProperties': {
                'pageObjectId': page_ids[page_id],
                'size': {
                    'height': emu4M,
                    'width': emu4M
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': 100000,
                    'translateY': 100000,
                    'unit': 'EMU'
                }
            },
            'url': IMAGE_URL
        }
    })

    # Execute the request.
    body = {
        'requests': requests
    }

    response = service.presentations().batchUpdate(presentationId=presentation_id,
                                                   body=body).execute()
    create_image_response = response.get('replies')[0].get('createImage')
    print('Created image with ID: {0}'.format(
        create_image_response.get('objectId')))
