import logging
import os

from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from gpush.auth import authenticate_service_account
from gpush.auth.services import ServicesBuilder, ServiceType
from gpush.request import (
    find_file,
    create_google_sheet,
    upload_data_to_sheet,
)
from gpush import __version__

# Set up logging and error handling
install_rich_traceback()
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

# Global Variables
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
FOLDER_ID = os.getenv("FOLDER_ID")

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def main(service_account_file, folder_id):
    """Main function to handle the Google Sheets operations."""
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    # Authenticate the service account
    credentials = authenticate_service_account(service_account_file, scopes)

    # Initialize Drive and Sheets services
    builder = ServicesBuilder(credentials)
    drive_service = builder.build(ServiceType.Drive)
    sheets_service = builder.build(ServiceType.Sheets)

    # File details
    file_name = "hello2"  # Name of the Google Sheets file

    # Find or create Google Sheet
    sheet_id = find_file(drive_service, folder_id, file_name)
    if not sheet_id:
        sheet_id = create_google_sheet(drive_service, folder_id, file_name)

    # Dummy data to upload
    dummy_data = [
        ["Name", "Age", "City"],
        ["Rachel", 30, "New York"],
        ["Bob", 25, "Maribor"],
        ["Charlie", 35, "London"],
    ]

    # Upload data to the sheet
    upload_data_to_sheet(sheets_service, sheet_id, dummy_data)
    logger.info("Data upload complete.")


if __name__ == "__main__":
    main(SERVICE_ACCOUNT_FILE, FOLDER_ID)
