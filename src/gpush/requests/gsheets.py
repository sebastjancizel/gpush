import logging
from typing import Any, List, Optional

from googleapiclient.discovery import Resource

from .utilities import error_handler

logger = logging.getLogger(__name__)


@error_handler
def upload_data_to_sheet(
    sheets_service: Resource,
    sheet_id: str,
    data: List[List[Any]],
    range_: Optional[str] = "Sheet1",
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
        upload_data_to_sheet(sheets_service, "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
                             [["Name", "Age"], ["John Doe", 30], ["Jane Doe", 25]], "Sheet1")

    Returns:
        None

    Raises:
        GoogleApiAccessError: If an error occurs while making the API request.
    """
    body = {"values": data}
    result = (
        sheets_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=sheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )
    logger.info(f"{result.get('updatedCells')} cells updated.")
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/"
    logger.info(f"Google Sheet can be found at: {sheet_url}")
