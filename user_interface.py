###############################################################
# User menu for selecting report type to generate
###############################################################

import exporters
import generators
from user_specific_extractor import login_google


## Presents menu and recives user input.
## Includes input verification.
def master_manu():
    print("Welcome to the she codes; report generator!")
    print("Select report to generate (enter number):\n"
          "1 - Weekly report\n"
          "2 - Compare to last year track opening\n"
          "3 - Single track opening report\n"
          "4 - Add track opening date\n")
    flag = 0
    while flag == 0:
        input_val = input()
        if input_val.isnumeric():
            if int(input_val)<5:
                return int(input_val)
            else:
                print("Number should appear in menu")
        else:
            print("Input should be a number")

## Executes actions according to user input selection
def menu_select(userInput):
    if userInput == 1:
        user_google_login_dict= login_google("user_specific.txt")
        weekly_report_dataframe, fig_names, fig_dir= generators.generator_weekly_report(user_google_login_dict)
        exporters.export_to_google_sheets(user_login_dict=user_google_login_dict, dataframe=weekly_report_dataframe,
                                          tab_name='Attendance Report')
        for k, fig in enumerate(fig_names):
            fig=fig.split(".")[0]
            exporters.export_figures_to_drive(user_login_dict=user_google_login_dict, figure_name=fig, figure_no=k)
        exporters.export_to_html(filename="Weekly Report", df_in_html=weekly_report_dataframe.to_html(), figure_names_list=fig_names,fig_dir=fig_dir)

    if userInput == 2:
        user_google_login_dict = login_google("user_specific.txt")
        fig_names, fig_dir = generators.generator_compare_last_year_report(user_sql_login_dict=user_google_login_dict)
        for k, fig in enumerate(fig_names):
            fig =fig.split(".")[0]
            exporters.export_figures_to_drive(user_login_dict=user_google_login_dict, figure_name=fig, figure_no=k)

    if userInput == 3:
        user_google_login_dict = login_google("user_specific.txt")
        activity_by_track_opening_selected_by_branch, fig_names, selected_reg_name = generators.generator_single_track_opening(user_sql_login_dict=user_google_login_dict)
        exporters.export_to_google_sheets(user_login_dict=user_google_login_dict,
                                          dataframe=activity_by_track_opening_selected_by_branch,
                                          tab_name=selected_reg_name+" by branch")
        for k, fig in enumerate(fig_names):
            fig=fig.split(".")[0]
            exporters.export_figures_to_drive(user_login_dict=user_google_login_dict, figure_name=fig, figure_no=k)

    if userInput == 4:
        print("Add it to track_opening.txt")

## Controles user interface components
def master_ui():
    user_input = master_manu()
    menu_select(user_input)
