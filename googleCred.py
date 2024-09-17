from config import SERVICE_ACCOUNT_CREDENTIALS
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_CREDENTIALS

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

form_service = discovery.build(
    "forms",
    "v1",
    credentials=credentials
)

form = {
    "info": {
        "title": "My really cool form",
    },
}

# Prints the details of the sample form
result = form_service.forms().create(body=form).execute()
print(result)
