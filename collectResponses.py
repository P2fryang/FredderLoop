import constants as c
import services as svc
from database import getFormId
from discordBot import collectResponsesMessage
from driveUtil import clear_nonowner_permissions, add_anyone_reader

if __name__ == "__main__":
    drive_service = svc.create_service(c.DRIVE_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    # remove all permissions (other than owning the file itself)
    clear_nonowner_permissions(drive_service=drive_service, file_id=formId)

    # add permission to view the files to anyone for submission
    add_anyone_reader(drive_service=drive_service, file_id=formId)

    collectResponsesMessage()
