import logging
from contextlib import contextmanager
from typing import Any, Generator, Optional

from googleapiclient.discovery import build

from gpush.auth.authenticator import authenticate_service_account


@contextmanager
def _temp_log_level(level: Any) -> Generator:
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


class Services:
    def __init__(self, service_account_path: Optional[str] = None) -> None:
        self.credentials = authenticate_service_account(service_account_path)
        with _temp_log_level(logging.ERROR):
            self.drive = build("drive", "v3", credentials=self.credentials)
            self.sheets = build("sheets", "v4", credentials=self.credentials)
