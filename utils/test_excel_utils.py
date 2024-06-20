import openpyxl

def read_excel(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    data = []
    for row in sheet.iter_rows(min_row=2,values_only=True): #values_only return  only cell values not  cell object
        data.append(row)
    return data
file_path = "C:\\Users\\Deepak\\PycharmProjects\\testing\\data\\logintestdata.xlsx"
sheet_name = "Sheet1"