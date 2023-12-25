from __future__ import annotations

import mimetypes
from typing import TYPE_CHECKING

from googleapiclient.http import MediaFileUpload  # type: ignore

from gpush import logger
from gpush.auth.services import Services
from gpush.requests.gdrive import find_file

if TYPE_CHECKING:
    from gpush.handlers.upload import FileDetails


def generic_handler(
    services: Services,
    folder_id: str,
    file: FileDetails,
) -> None:
    """Uploads any file type to Google Drive."""
    name = file.name
    path = file.path

    # Determine the MIME type of the file
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        # Fallback MIME type or handling if MIME type cannot be determined
        mime_type = "application/octet-stream"

    # Check if the file exists
    if find_file(services.drive, folder_id, name):
        logger.warning(f"File {name} already exists in the folder.")

    file_metadata = {"name": name, "mimeType": mime_type, "parents": [folder_id]}

    media = MediaFileUpload(path, mimetype=mime_type)

    result = (
        services.drive.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    # Retrieve the file ID from the upload result
    file_id = result.get("id")

    # Construct the URL to access the file on Google Drive
    file_url = f"https://drive.google.com/file/d/{file_id}/view"

    # Log the file name, ID, and URL
    logger.info(f"File '{name}' uploaded; URL: {file_url}")
