from googleCred import credentials
from apiclient import discovery

from database import getFormId
from discordBot import shareResponsesMessage

if __name__ == "__main__":
    form_service = discovery.build("forms", "v1", credentials=credentials)
    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    formId = getFormId()
    if formId == "":
        exit()

    # add permission to view the files only to the people who responded
    responses = form_service.forms().responses().list(formId=formId).execute()

    for response in responses['responses']:
        if 'respondentEmail' not in response:
            print("Ah! The form didn't collect email addresses :(")
            continue

        email = response['respondentEmail']
        drive_service.permissions().create(
            fileId=formId,
            body={
                "type": "user",
                "emailAddress": email,
                "role": "writer"
            }
        ).execute()

        print("added writer role for", email)

    shareResponsesMessage()
