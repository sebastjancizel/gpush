from __future__ import annotations

import os
from argparse import Namespace
from dataclasses import dataclass
from enum import Enum

from gpush import logger
from gpush.auth.services import Services
from gpush.requests.gdrive import create_drive_folder

from .generic import generic_handler
from .spreadsheet import spreadsheet_handler


class UploadType(Enum):
    CSV = ".csv"
    XLSX = ".xlsx"
    XLS = ".xls"
    DIR = ""
    OTHER = "other"

    @staticmethod
    def from_path(path: str) -> UploadType:
        # get base and extension of file
        _, ext = os.path.splitext(os.path.basename(path))

        match ext:
            case "" if os.path.isdir(path):
                return UploadType.DIR
            case "":
                return UploadType.OTHER
            case _:
                try:
                    return UploadType(ext)
                except ValueError:
                    return UploadType.OTHER


@dataclass
class FileDetails:
    path: str
    name: str
    sheet: str
    type: UploadType

    @staticmethod
    def from_args(args: Namespace) -> FileDetails:
        return FileDetails(
            path=args.path,
            name=args.name if args.name else os.path.basename(args.path),
            sheet=args.sheet,
            type=UploadType.from_path(args.path),
        )


def dir_handler(services: Services, folder_id: str, file: FileDetails) -> None:
    logger.debug(f"Create directory {file.name}...")

    new_folder_id = create_drive_folder(services.drive, file.name, folder_id)

    for f in os.listdir(file.path):
        logger.info(f"Uploading {f}...")
        new_path = os.path.join(file.path, f)

        new_file = FileDetails(
            path=new_path,
            name=f,
            type=UploadType.from_path(new_path),
            sheet=file.sheet,
        )

        # Recursively upload files in the directory
        upload_file(services, new_folder_id, new_file)


def upload_file(services: Services, folder_id: str, file: FileDetails) -> None:
    match file.type:
        case UploadType.CSV | UploadType.XLSX | UploadType.XLS:
            spreadsheet_handler(services, folder_id, file)
        case UploadType.DIR:
            dir_handler(services, folder_id, file)
        case _:
            generic_handler(services, folder_id, file)
