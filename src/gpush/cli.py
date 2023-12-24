import csv
import logging
import os
from argparse import ArgumentParser, Namespace

from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from gpush.auth import authenticate_service_account
from gpush.auth.services import ServicesBuilder, ServiceType
from gpush.requests.gdrive import create_google_sheet, find_file
from gpush.requests.gsheets import upload_data_to_sheet

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


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="gpush",
        description="A CLI tool to upload data to Google Sheets.",
    )

    parser.add_argument(
        "--path",
        "-p",
        type=str,
        help="Path to the file to be uploaded.",
        required=True,
    )

    parser.add_argument(
        "--name",
        "-n",
        type=str,
        help="Name of the Google Sheet.",
        required=False,
    )

    args = parser.parse_args()
    if args.name is None:
        args.name = os.path.basename(args.path).split(".")[0]

    return args


def main():
    args = parse_args()
    file_name = args.name

    """Main function to handle the Google Sheets operations."""
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    # Authenticate the service account
    credentials = authenticate_service_account(SERVICE_ACCOUNT_FILE, scopes)

    # Initialize Drive and Sheets services
    builder = ServicesBuilder(credentials)
    drive_service = builder.build(ServiceType.Drive)
    sheets_service = builder.build(ServiceType.Sheets)

    # Find or create Google Sheet
    sheet_id = find_file(drive_service, FOLDER_ID, file_name)
    if not sheet_id:
        sheet_id = create_google_sheet(drive_service, FOLDER_ID, file_name)

    # Read data from a csv file at the given path and convert it to a list of lists
    path = args.path
    with open(path) as f:
        dummy_data = list(csv.reader(f))
        logger.info(dummy_data)

    # Upload data to the sheet
    upload_data_to_sheet(sheets_service, sheet_id, dummy_data)
    logger.info("Data upload complete.")


if __name__ == "__main__":
    main()
