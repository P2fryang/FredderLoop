from googleCred import credentials
from apiclient import discovery

from database import getFormId
from discordBot import shareResponsesMessage

if __name__ == "__main__":
    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    formId = getFormId()
    if formId === "":
        exit()

    # remove all permissions (other than owning the file itself)
    result = drive_service.permissions().list(
        fileId=formId,
    ).execute()

    print(result['permissions'])

    # add permission to view the files
    drive_service.permissions().update(
        fileId=formId,
        permissionId="anyoneWithLink",
        body={
            "role": "writer"
        }
    ).execute()

    shareResponsesMessage()
