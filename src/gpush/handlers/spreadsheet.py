import csv

from gpush.requests.gdrive import create_google_sheet, find_file
from gpush.requests.gsheets import upload_data_to_spreadsheet


def spreadsheet_handler(services, folder_id, file):
    """Uploads a file to a Google Sheet."""
    # Check if the file exists
    file_id = find_file(services.drive, folder_id, file.name)
    if not file_id:
        file_id = create_google_sheet(services.drive, folder_id, file.name)

    with open(file.path) as f:
        dummy_data = list(csv.reader(f))

    # Upload data to the sheet
    upload_data_to_spreadsheet(services.sheets, file_id, dummy_data)
