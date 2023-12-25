from dataclasses import dataclass

from .upload import Extension, upload_file  # noqa: F401


@dataclass
class FileDetails:
    path: str
    name: str
    sheet: str
    ext: Extension
