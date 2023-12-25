import logging
import os
from argparse import ArgumentParser

from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from gpush.auth.services import Services
from gpush.handlers import Extension, FileDetails, upload_file

# Set up logging and error handling
install_rich_traceback()
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args() -> FileDetails:
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
        help="Desired name of the upload. Defaults to the name of the file",
        required=False,
    )

    parser.add_argument(
        "--sheet",
        "-s",
        type=str,
        help="Name of the specific sheet within the Google Sheet. Only applicable to spreadsheets.",
        required=False,
        default="Sheet1",  # Default sheet name
    )

    args = parser.parse_args()
    base, ext = os.path.splitext(os.path.basename(args.path))

    file = FileDetails(
        path=args.path,
        name=args.name or base,
        ext=Extension.from_string(ext),
        sheet=args.sheet,
    )

    return file


def main():
    file = parse_args()
    logger.info(f"Uploading {file.path} to Google Drive/Sheets as {file.name}...")

    services = Services()
    folder_id = os.getenv("FOLDER_ID")

    upload_file(services, folder_id, file)
    logger.info("Data upload complete.")


if __name__ == "__main__":
    main()
