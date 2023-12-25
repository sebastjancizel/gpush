import mimetypes

from googleapiclient.http import MediaFileUpload  # type: ignore

from gpush.auth.services import Services
from gpush.handlers import FileDetails
from gpush.requests.gdrive import find_file


def spreadsheet_handler(
    services: Services,
    folder_id: str,
    file: FileDetails,
):
    """Uploads any file type to Google Drive."""
    name = file.name
    path = file.path

    # Determine the MIME type of the file
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        # Fallback MIME type or handling if MIME type cannot be determined
        mime_type = "application/octet-stream"

    # Check if the file exists
    file_id = find_file(services.drive, folder_id, name)

    file_metadata = {"name": name, "mimeType": mime_type, "parents": [folder_id]}

    media = MediaFileUpload(path, mimetype=mime_type)
    if file_id:
        # Update the existing file
        (
            services.drive.files()
            .update(fileId=file_id, body=file_metadata, media_body=media)
            .execute()
        )
    else:
        # Upload as a new file
        (
            services.drive.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
