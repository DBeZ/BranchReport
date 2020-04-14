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
    if userInput ==1:
        generators.generator_weekly_report()
    if userInput ==2:
        print("Add date weekly_calender.py (quarterly_reg_dates function)")

## Controles user interface components
def master_ui():
    user_input = master_manu()
    menu_select(user_input)
