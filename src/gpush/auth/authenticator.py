from google.oauth2 import service_account


def authenticate_service_account(service_account_file, scopes):
    """Authenticate the service account and return the credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    return credentials
