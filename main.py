###############################################################
# she codes; report system for HQ
# By: Doreen Ben-Zvi
###############################################################
# Please note all security certificates should be stored in a parallel folder to the project.
# i.e. if the project file is C:\PycharmProjects\shecodes_hq_reports
# the certificates should be in C:\PycharmProjects\User_specific_security_files

from user_interface import master_ui
import os

def main():
    master_ui()

# Make sure main cannot be called from other functions
if __name__ == "__main__":
    main()
