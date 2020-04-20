import exporters
import generators
from user_specific_extractor import login_google


## Presents menu and recives user input.
## Includes input verification.
def master_manu():
    print("Welcome to the she codes; report generator!")
    print("Select report to generate (enter number):\n"
          "1 - Weekly report\n"
          "2 - Add track opening date\n")
    flag = 0
    while flag == 0:
        input_val = input()
        if input_val.isnumeric():
            if int(input_val)<3:
                return int(input_val)
            else:
                print("Number should appear in menu")
        else:
            print("Input should be a number")

## Executes actions according to user input
def menu_select(userInput):
    if userInput == 1:
        user_login_dict = login_google()
        weekly_report_dataframe, fig_names = generators.generator_weekly_report(user_login_dict)
        exporters.export_to_google_sheets(user_login_dict, dataframe=weekly_report_dataframe,
                                          tab_name='Attendance Report')
        for k, fig in enumerate(fig_names):
            exporters.export_figures_to_drive(user_login_dict=user_login_dict, figure_name=fig, figure_no=k)

    if userInput == 2:
        print("Add date weekly_calender.py (quarterly_reg_dates function)")

## Controles user interface components
def master_ui():
    user_input = master_manu()
    menu_select(user_input)
