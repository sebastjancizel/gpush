from enum import Enum

from googleapiclient.discovery import build, Resource
import logging
from contextlib import contextmanager


@contextmanager
def _temp_log_level(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


class ServiceType(Enum):
    Drive = "drive"
    Sheets = "sheets"


class ServicesBuilder:
    def __init__(self, credentials) -> None:
        self.credentials = credentials

    def build(self, service_type: ServiceType) -> Resource:
        with _temp_log_level(logging.ERROR):
            match service_type:
                case ServiceType.Drive:
                    return build("drive", "v3", credentials=self.credentials)
                case ServiceType.Sheets:
                    return build("sheets", "v4", credentials=self.credentials)
                case _:
                    raise ValueError(f"Invalid service type: {service_type}")
