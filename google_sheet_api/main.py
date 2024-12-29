import gspread
from google.oauth2.service_account import Credentials

scopes =[
    'https://www.googleapis.com/auth/spreadsheets',
]

creds = Credentials.from_service_account_file("Credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1lxMsC-XS5pFxXBzQ3b__yzuAUjdvqpq5EJKRYYIDoMY"
workbook = client.open_by_key(sheet_id)
sheet_name = 'tutor_sheet'

values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
]

worksheet_list = list(map(lambda x:x.title, workbook.worksheets()))

if sheet_name in worksheet_list:
    sheet = workbook.worksheet(sheet_name)
else:
    sheet = workbook.add_worksheet(sheet_name, rows=10, cols=10)


sheet.update(f"A1:C{len(values)}", values)

sheet.update_cell(len(values) + 1, 2, f"=sum(B2:B{len(values)})")
sheet.update_cell(len(values) + 1, 3, f"=sum(C2:C{len(values)})")

sheet.format("A1:C1", {"textFormat": {"bold": True}})