import logging
import os
from contextlib import contextmanager
from typing import Any, Generator, Optional

from google.oauth2.service_account import Credentials  # type: ignore
from googleapiclient.discovery import build  # type: ignore

logger = logging.getLogger(__name__)


class MissingServiceAccountFile(Exception):
    pass


@contextmanager
def _temp_log_level(level: Any) -> Generator:
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


def _read_service_account_file() -> str:
    logger.debug(
        "Reading service account file from SERVICE_ACCOUNT_FILE environment variable."
    )
    service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")

    if not service_account_file:
        raise MissingServiceAccountFile(
            "Unable to locate service account file. "
            "gpush looks for the file path in the SERVICE_ACCOUNT_FILE environment variable; "
            "please ensure that it is set to a valid path."
        )
    return service_account_file


def authenticate_service_account(
    service_account_file: Optional[str] = None,
) -> Credentials:
    """Authenticate the service account and return the credentials."""

    if not service_account_file:
        service_account_file = _read_service_account_file()

    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    credentials = Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes,
    )
    return credentials


class Services:
    def __init__(self, service_account_path: Optional[str] = None) -> None:
        self.credentials = authenticate_service_account(service_account_path)
        with _temp_log_level(logging.ERROR):
            self.drive = build("drive", "v3", credentials=self.credentials)
            self.sheets = build("sheets", "v4", credentials=self.credentials)
