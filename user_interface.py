import exporters
import generators


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
        result_file_name = "Weekly Report"
        weekly_report_dataframe, fig_names = generators.generator_weekly_report()
        exporters.export_to_google_sheets(dataframe=weekly_report_dataframe, sheets_file_name=result_file_name,
                                          tab_name='Attendance Report')
        k = 0
        for fig in fig_names:
            k += 1
            exporters.export_figures_to_drive(figure_name=fig)
            # exporters.insert_figure_image_to_sheet(image_file_name=fig, sheets_file_name=result_file_name, tab_name='Attendance Graphs')
            exporters.insert_figure_image_to_slides(figure_name=fig, slides_file_name=result_file_name, page_id=k)
    if userInput == 2:
        print("Add date weekly_calender.py (quarterly_reg_dates function)")

## Controles user interface components
def master_ui():
    user_input = master_manu()
    menu_select(user_input)
