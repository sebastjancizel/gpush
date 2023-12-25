import os
from argparse import ArgumentParser

from gpush import logger
from gpush.auth.services import Services
from gpush.handlers.upload import Extension, FileDetails, upload_file

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


def main() -> None:
    file = parse_args()
    logger.info(f"Uploading {file.path} to Google Drive/Sheets as {file.name}...")

    services = Services()
    folder_id = os.getenv("FOLDER_ID")

    if folder_id is None:
        raise ValueError("FOLDER_ID environment variable is not set.")

    upload_file(services, folder_id, file)
    logger.info("Data upload complete.")


if __name__ == "__main__":
    main()
