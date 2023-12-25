from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum

from gpush import logger
from gpush.auth.services import Services
from gpush.requests.gdrive import create_drive_folder

from .generic import generic_handler
from .spreadsheet import spreadsheet_handler


class Extension(Enum):
    CSV = ".csv"
    XLSX = ".xlsx"
    XLS = ".xls"
    DIR = ""
    OTHER = "other"

    @staticmethod
    def from_string(s: str) -> Extension:
        try:
            return Extension(s)
        except ValueError:
            return Extension.OTHER


@dataclass
class FileDetails:
    path: str
    name: str
    sheet: str
    ext: Extension


def dir_handler(services: Services, folder_id: str, file: FileDetails) -> None:
    logger.debug(f"Create directory {file.name}...")

    new_folder_id = create_drive_folder(services.drive, file.name, folder_id)

    for f in os.listdir(file.path):
        logger.info(f"Uploading {f}...")

        new_file = FileDetails(
            path=os.path.join(file.path, f),
            name=f,
            ext=Extension.from_string(os.path.splitext(f)[1]),
            sheet=file.sheet,
        )

        upload_file(services, new_folder_id, new_file)


def upload_file(services: Services, folder_id: str, file: FileDetails) -> None:
    match file.ext:
        case Extension.CSV | Extension.XLSX | Extension.XLS:
            spreadsheet_handler(services, folder_id, file)
        case Extension.DIR:
            dir_handler(services, folder_id, file)
        case _:
            generic_handler(services, folder_id, file)
