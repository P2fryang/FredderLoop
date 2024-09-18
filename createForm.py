from googleCred import credentials
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from datetime import datetime


form_service = discovery.build("forms", "v1", credentials=credentials)
drive_service = discovery.build('drive', 'v3', credentials=credentials)

def createForm(folder_id):

    # create the form
    date = datetime.today().strftime('%Y-%m-%d')
    form = form_service.forms().create(
        body={
            "info": {
                "title": date + " LetterLoop Questions",
                "documentTitle": date
            }
        }
    ).execute()
    formId = form['formId']

    # add default questions
    form_service.forms().batchUpdate(
        formId=formId,
        body={
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": "What is your name",
                            "description": "Please give me your name",
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False
                                    }
                                }
                            }
                        },
                        "location": {
                            "index": 0
                        }
                    }
                },
                {
                    "createItem": {
                        "item": {
                            "title": "Alright! Here's a letter loop question",
                            "description": "",
                            "questionItem": {
                                "question": {
                                    "textQuestion": {
                                        "paragraph": True
                                    }
                                }
                            }
                        },
                        "location": {
                            "index": 1
                        }
                    }
                }
            ]
        }
    ).execute()

    # set form editing permissions to anyone with the link
    drive_service.permissions().create(
        fileId=formId,
        body={
            'type': 'anyone',
            'role': 'writer',
        }
    ).execute()

    # Move the form to specific folderId
    prevParents = ",".join(drive_service.files().get(
        fileId=formId,
        fields='parents'
    ).execute()['parents'])

    file = drive_service.files().update(
        fileId=formId,
        addParents=folder_id,
        removeParents=prevParents,
        fields='id, parents'
    ).execute()

    return form



form = createForm("1lPkEZ8CHA5IeQJ10wg2ZbCo6IlRkgqiD")
print(form)
