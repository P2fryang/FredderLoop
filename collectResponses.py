from apiclient import discovery

from googleCred import credentials
from database import getFormId
from discordBot import collectResponsesMessage

if __name__ == "__main__":
    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    formId = getFormId()
    if formId === "":
        exit()

    # remove all permissions (other than owning the file itself)
    result = drive_service.permissions().list(
        fileId=formId,
    ).execute()

    for permission in result['permissions']:
        if permission['role'] != 'owner':
            drive_service.permissions().delete(
                fileId=formId,
                permissionId=permission['id']
            ).execute()

            print('removing', permission)

    # add permission to view the files
    drive_service.permissions().create(
        fileId=formId,
        body={
            "type": "anyone",
            "role": "reader"
        }
    ).execute()

    collectResponsesMessage()
