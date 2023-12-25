from enum import Enum

from .generic import generic_handler
from .spreadsheet import spreadsheet_handler


class Extension(Enum):
    CSV = ".csv"
    XLSX = ".xlsx"
    XLS = ".xls"
    HTML = ".html"
    MP4 = ".mp4"
    OTHER = "other"

    @staticmethod
    def from_string(s: str) -> "Extension":
        try:
            return Extension(s)
        except KeyError:
            return Extension.OTHER


def upload_file(services, folder_id, file):
    match file.ext:
        case Extension.CSV | Extension.XLSX | Extension.XLS:
            spreadsheet_handler(services, folder_id, file)
        case _:
            generic_handler(services, folder_id, file)
