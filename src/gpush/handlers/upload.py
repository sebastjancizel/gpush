from enum import Enum

from .generic import generic_handler
from .spreadsheet import spreadsheet_handler


class Ext(Enum):
    CSV = ".csv"
    XLSX = ".xlsx"
    XLS = ".xls"
    OTHER = "other"

    @staticmethod
    def from_string(s: str):
        try:
            return Ext(s)
        except KeyError:
            return Ext.OTHER


def upload_file(services, folder_id, file):
    match file.ext:
        case Ext.CSV | Ext.XLSX | Ext.XLS:
            spreadsheet_handler(services, folder_id, file)
        case Ext.OTHER:
            generic_handler(services, folder_id, file)
