import logging
from typing import Optional

from googleapiclient.discovery import Resource  # type: ignore

from .utilities import error_handler

logger = logging.getLogger(__name__)


@error_handler
def find_file(
    drive_service: Resource,
    folder_id: str,
    file_name: str,
) -> Optional[str]:
    """
    Search for a file with a specific name in a given Google Drive folder.

    This function uses the Google Drive API to search for a file with the specified name
    within the folder identified by `folder_id`. If the file is found, its ID is returned.
    If no file is found, the function returns None.

    Args:
        drive_service (Resource): A Resource object representing the Google Drive API service.
        folder_id (str): The ID of the Google Drive folder to search in.
        file_name (str): The name of the file to search for.

    Returns:
        Optional[str]: The ID of the found file, or None if no file was found.

    Raises:
        GoogleApiAccessError: If any error occurs during the API request.
    """

    query = f"'{folder_id}' in parents and trashed = false"
    response = (
        drive_service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    files = response.get("files", [])

    for file in files:
        if file.get("name") == file_name:
            logger.debug(f"File found with ID: {file.get('id')}")
            return file.get("id")
    return None


@error_handler
def create_google_sheet(
    drive_service: Resource,
    folder_id: str,
    file_name: str,
) -> str:
    """
    Create a new Google Sheet in the specified folder.

    This function creates a new Google Sheet with the specified name in the specified folder.
    The MIME type is set as 'application/vnd.google-apps.spreadsheet' which designates the file to be a Google Sheet.
    The ID of the newly created file is returned.

    Args:
        drive_service (Resource): The Google Drive API service instance.
        folder_id (str): The ID of the folder where the new Google Sheet will be created.
        file_name (str): The name of the new Google Sheet.

    Returns:
        str: The ID of the newly created Google Sheet.

    Raises:
        GoogleApiAccessError: If any error occurs during the API request.
    """
    file_metadata = {
        "name": file_name,
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [folder_id],
    }
    file = (
        drive_service.files()
        .create(
            body=file_metadata,
            fields="id",
        )
        .execute()
    )
    logger.info(f"Created new Google Sheets File ID: {file.get('id')}")

    return file.get("id")


@error_handler
def create_drive_folder(
    drive_service: Resource,
    folder_name: str,
    parent_folder_id: str,
) -> str:
    """
    Create or find a folder within a specific Google Drive folder.

    This function creates a new folder with the given name within the specified parent folder
    on Google Drive. If a folder with the same name already exists in the parent folder,
    it returns the ID of the existing folder. Otherwise, it creates a new folder and
    returns its ID.

    Args:
        drive_service (Resource): The Google Drive API service instance.
        folder_name (str): The name of the folder to be created or found.
        parent_folder_id (str): The ID of the parent folder where the folder will be created or searched.

    Returns:
        str: The ID of the created or found folder.

    Raises:
        GoogleApiAccessError: If any error occurs during the API request.
    """

    # Check if the folder already exists
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents and trashed = false"
    response = (
        drive_service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    files = response.get("files", [])

    if files:
        folder_id = files[0].get("id")
        logger.debug(f"Folder '{folder_name}' already exists with ID: {folder_id}")
        return folder_id

    # Folder does not exist, create a new one
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id],
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    folder_id = folder.get("id")
    logger.debug(f"Created new folder '{folder_name}' with ID: {folder_id}")

    return folder_id
