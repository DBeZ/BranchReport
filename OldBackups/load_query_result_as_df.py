################################################
# Loads file containing query results
################################################

import pandas as pd


def load_query_result_as_df(filename, sheet=0):
    if type(filename) is not str:
        filename = str(filename)
    fileExt = str.split(filename, ".")[1]
    if fileExt == "csv":
        data = pd.read_csv(filename)
    elif (fileExt == "xlsx") or (fileExt == "xls"):
        if type(sheet) is not str:
            sheet = str(sheet)
        data = pd.read_excel(io=filename, sheet_name=sheet)
    elif fileExt == "html":
        data = pd.read_html(filename)
    elif fileExt == "json":
        data = pd.read_json(filename)
    else:
        raise Exception('Filetype cannot be loaded')
    return data
