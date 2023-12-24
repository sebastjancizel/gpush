import logging
from typing import Any, List, Optional

from googleapiclient.discovery import Resource

from .utilities import error_handler

logger = logging.getLogger(__name__)


@error_handler
def check_or_create_sheet(
    sheets_service: Resource,
    spreadsheet_id: str,
    sheet_name: str,
) -> None:
    """
    Check if a sheet exists in the given spreadsheet, and create it if it doesn't.

    Args:
        sheets_service (Resource): The Google Sheets API service instance.
        spreadsheet_id (str): The ID of the Google Sheet.
        sheet_name (str): The name of the sheet to check or create.
    """
    # Get the list of sheets in the spreadsheet
    sheet_metadata = (
        sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    )
    sheets = sheet_metadata.get("sheets", "")

    # Check if the sheet exists
    if not any(sheet["properties"]["title"] == sheet_name for sheet in sheets):
        # If the sheet does not exist, create it
        body = {"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]}
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body
        ).execute()
        logger.debug(f"Created new sheet: {sheet_name}")
    else:
        logger.debug(f"Found existing sheet: {sheet_name}")


@error_handler
def upload_data_to_spreadsheet(
    sheets_service: Resource,
    spreadsheet_id: str,
    data: List[List[Any]],
    sheet: Optional[str] = "Sheet2",
) -> None:
    """
    Upload data to the specified Google Sheet.

    This function uploads the provided data to the specified Google Sheet.
    The data is provided as a list of lists, where each inner list represents a row of data.

    Args:
        sheets_service (Resource): The Google Sheets API service instance.
        sheet_id (str): The ID of the Google Sheet to update.
        data (List[List[Any]]): The data to upload. Each inner list represents a row of data.
        range_ (str, optional): The A1 notation of the values to update. Defaults to "Sheet1".

    Example:
        upload_data_to_sheet(sheets_service, "123456", [["Name", "Age"], ["John Doe", 30], ["Jane Doe", 25]], "Sheet1")

    Returns:
        None

    Raises:
        GoogleApiAccessError: If an error occurs while making the API request.
    """
    # Check if the sheet exists or create it
    check_or_create_sheet(sheets_service, spreadsheet_id, sheet)

    body = {"values": data}
    result = (
        sheets_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=sheet,  # range means a sheet in this case
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )
    logger.debug(f"{result.get('updatedCells')} cells updated.")
    sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/"
    logger.info(f"Google Sheet can be found at: {sheet_url}")
