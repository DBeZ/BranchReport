##################################################################################
# Connect to google drive, upload files to it, write into sheets and slides files
##################################################################################
# Using this requires:
# 1. Enabling APIs (drive, sheets, slides)in the drive
# 2. Generating certificate:
#   1.1 client_secrets.json for drive login
#   1.2 API_login.json for sheets and slides
#   1.3 Both should be in \PycharmProjects\User_specific_security_files in parallel to \PycharmProjects\shecodes_hq_reports
# 2. Open a dedicated folder in the drive and update its ID in "user_specific.txt"
#       The folder ID is in its URL after /folders/
# 3. Sheets and Slides files need to be opened in the drive. Update their IDs in "user_specific.txt"
#       The file ID is in its URL between /d/ and /edit
# 4. Set "Anyone who has the link can view" to the drive and all the files therein


import gspread
from df2gspread import df2gspread as d2g
from oauth2client import service_account, client, tools
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from googleapiclient.discovery import build
import httplib2
from random import seed
from random import randint
import os
from webbrowser import open_new_tab
import wrappers

# TODO: if file exists update it. If not create it. Then write into it
# Exports dataframe by copying it as-is into a sheets tab
def export_to_google_sheets(user_login_dict, dataframe, tab_name):
    spreadsheet_id = user_login_dict["spreadsheet_id"]
    wks_name = tab_name
    scope = ['https://www.googleapis.com/auth/spreadsheets'] #Sets files that can be access on the drive.
    try:
        working_folder = os.getcwd()
        os.chdir("..")
        os.chdir(user_login_dict["certificates_folder"])
        jsonFile = user_login_dict["api_login_json"]
        credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
            jsonFile, scope)
        gc = gspread.authorize(credentials)
        os.chdir("..")
        d2g.upload(dataframe, spreadsheet_id, wks_name, credentials=credentials, row_names=True) #TODO change so int and not str are uploaded into sheet
        os.chdir(working_folder)
        print("Export to google sheets complete")
    except:
        os.chdir(working_folder)
        print("Export to google sheets failed")
        print("Report will be saved instead")
        export_to_csv(dataframe, user_login_dict["result_file_name"])


# Saves a dataframe as a local CSV file
def export_to_csv(dataframe, report_name):
    now = str(datetime.now().strftime("%y%m%d %H_%M"))
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    dataframe.to_csv(os.getcwd() + "\\" + report_name + now + ".csv", index=True, header=True)
    os.chdir("..")
    print("Results saved as csv")

# TODO: if file exists update it. If not create it. Then write into it

# Insert image into an existing slides file.
# ALL SLIDES REQUIRED MUST ALREADY EXIST. It does not add slides to a presentation
#  TODO if a fig exists in the slide update it, if not insert it
def insert_figure_image_to_slides(user_login_dict, figure_url, page_id):
    presentation_id = user_login_dict["presentation_id"]
    jsonFile = user_login_dict["api_login_json"]
    scope = 'https://www.googleapis.com/auth/presentations'
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
        # Backup of setting image size in the slide
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

        #
        # print('Created image with ID: {0}'.format(create_image_response.get('objectId')))

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
        fig_url=file_on_drive.get('webContentLink')

    except:
        os.chdir(working_folder)
        print("Error uploading file to drive")

    insert_figure_image_to_slides(user_login_dict=user_login_dict, figure_url=fig_url, page_id=figure_no)

def export_to_html(filename, df_in_html, figure_names_list, fig_dir):
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    f = open(filename+'.html','w')
    whole = wrappers.weekly_report_wrapper(df_in_html, figure_names_list, fig_dir)
    f.write(whole)
    f.close()
    os.chdir("..")



#Drive access using flow opens browser for confirmatiop each access request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from oauth2client.file import Storage
#         store = Storage(user_login_dict["drive_login_json"])
#         flow = client.flow_from_clientsecrets(user_login_dict["drive_login_json"], scopes)



# No longer supported by sheet api
# def insert_figure_image_to_sheet(image_file_name, sheets_file_name, tab_name):
#     image_url="https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Fpenguin-images-free.html&psig=AOvVaw1_6tqfSRpyq7FcNqAveEpD&ust=1587332101390000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOi1g4L38ugCFQAAAAAdAAAAABAD"
#
#     os.chdir(str("User_specific_files"))
#     jsonFile = 'API_login.json'  # Name of file downloaded when API is enabled on drive
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
#         jsonFile, scope)  # load credentials from json file
#     gc = gspread.authorize(credentials)
#     worksheets = gc.open(sheets_file_name).worksheets()
#     for worksheet in worksheets:
#         if worksheet.title =='Attendance Graphs':
#             # worksheet.append_row([image_file_name, '=IMAGE(\"{}\")'.format(image_url)], 'USER_ENTERED')
#
#             worksheet.append_row([image_file_name, '=IMAGE(\"{}\")'.format(image_url)])
#     os.chdir("..")
#

