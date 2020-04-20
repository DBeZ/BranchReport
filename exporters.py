import gspread
from df2gspread import df2gspread as d2g
from oauth2client import service_account, client, tools
from oauth2client.file import Storage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
import httplib2
from random import seed
from random import randint

import os


def export_to_google_sheets(user_login_dict, dataframe, tab_name):
    spreadsheet_id = user_login_dict["spreadsheet_id"]
    wks_name = tab_name
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    try:
        working_folder = os.getcwd()
        os.chdir("..")
        os.chdir(user_login_dict["certificates_folder"])
        jsonFile = user_login_dict["api_login_json"]
        credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
            jsonFile, scope)
        gc = gspread.authorize(credentials)
        os.chdir("..")
        d2g.upload(dataframe, spreadsheet_id, wks_name, credentials=credentials, row_names=True)
        os.chdir(working_folder)
        print("Export to google sheets complete")
    except:
        os.chdir(working_folder)
        print("Export to google sheets failed")
        print("Report will be saved instead")
        export_to_csv(dataframe, user_login_dict["result_file_name"])


def export_to_csv(dataframe, report_name):
    now = str(datetime.now().strftime("%y%m%d %H_%M"))
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    dataframe.to_csv(os.getcwd() + "\\" + report_name + now + ".csv", index=True, header=True)
    os.chdir("..")
    print("Results saved as csv")


def insert_figure_image_to_slides(user_login_dict, figure_url, page_id):
    presentation_id = user_login_dict["presentation_id"]
    jsonFile = user_login_dict["api_login_json"]
    scope = 'https://www.googleapis.com/auth/presentations'  # , 'https://www.googleapis.com/auth/drive.file'
    seed(randint(page_id, 101))
    id = randint(1, 100000)
    image_id = "Figure" + str(id)

    try:
        working_folder = os.getcwd()
        os.chdir("..")
        os.chdir(user_login_dict["certificates_folder"])
        credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(jsonFile, scopes=scope)
        os.chdir(working_folder)

        service = build('slides', 'v1', http=credentials.authorize(httplib2.Http()), cache_discovery=False)
        slides = service.presentations().get(presentationId=presentation_id,
                                             fields='slides').execute().get('slides')
        page_ids = []
        for slide in slides:
            page_ids.append(slide['objectId'])

        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        requests = []
        requests.append({
            'createImage': {
                'objectId': image_id,
                'elementProperties': {
                    'pageObjectId': page_ids[page_id]
                },
                'url': figure_url
            }
        })
        #     requests.append({
        #     'createImage': {
        #         'objectId': image_id,
        #         'elementProperties': {
        #             'pageObjectId': page_ids[page_id],
        #             'size': {
        #                 'height': emu4M,
        #                 'width': emu4M
        #             },
        #             'transform': {
        #                 'scaleX': 1,
        #                 'scaleY': 1,
        #                 'translateX': 100000,
        #                 'translateY': 100000,
        #                 'unit': 'EMU'
        #             }
        #         },
        #         'url': figure_url
        #     }
        # })
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=presentation_id,
                                                       body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')

        print('Created image with ID: {0}'.format(
            create_image_response.get('objectId')))

    except:
        os.chdir(working_folder)
        print("Image insertion into presentation failed")


def export_figures_to_drive(user_login_dict, figure_name, figure_no):
    drive_folder_id = user_login_dict["drive_folder_id"]
    file_name = figure_name + ".png"
    scopes = (
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/presentations',
    )

    os.chdir("Output_files")
    output_dir = os.getcwd()
    os.chdir("..")

    try:
        working_folder = os.getcwd()
        os.chdir("..")
        os.chdir(user_login_dict["certificates_folder"])
        g_login = GoogleAuth(user_login_dict["drive_login_yaml"])
        g_login.LocalWebserverAuth()

        store = Storage(user_login_dict["drive_login_json"])
        flow = client.flow_from_clientsecrets(user_login_dict["drive_login_json"], scopes)

        os.chdir(working_folder)
        drive = GoogleDrive(g_login)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == user_login_dict["result_file_name"]:
                folder_id = file.get('id')

        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file1 in file_list:
            if file1['title'] == file_name:
                file1.Delete()

        os.chdir(output_dir)
        file_on_drive = drive.CreateFile({'parents': [{'id': drive_folder_id}]})
        file_on_drive.SetContentFile(file_name)
        file_on_drive.Upload()
        os.chdir(working_folder)
        print('Graph Export to drive complete - %s' % (file_name))
        metadata = file_on_drive.attr["metadata"]
        fig_url4 = metadata["alternateLink"]
        fig_url5 = metadata['selfLink']
        fig_url6 = metadata['webContentLink']
        fig_url7 = metadata['downloadUrl']
    except:
        os.chdir(working_folder)
        print("Error uploading file to drive")

    creds = tools.run_flow(flow, store)  # opens browser identificaiton page
    HTTP = creds.authorize(httplib2.Http())
    DRIVE = discovery.build('drive', 'v3', http=HTTP)
    rsp = DRIVE.files().list(q="name='%s'" % file_name).execute().get('files')[0]

    fig_url1 = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
    fig_url2 = "https://drive.google.com/uc?export=download&id=" + rsp["id"]
    fig_url3 = '%s&access_token=%s' % (DRIVE.files().get_media(fileId=rsp['id']).uri, creds.access_token)
    fig_url8 = "https://drive.google.com/file/d/1AmCmoc8Xrv706yJeWCmCuQw0HQkkYHpQ/view?usp=sharing"

    insert_figure_image_to_slides(user_login_dict=user_login_dict, figure_url=fig_url1, page_id=figure_no)


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
