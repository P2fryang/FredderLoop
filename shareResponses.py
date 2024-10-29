from googleCred import credentials
from apiclient import discovery

from database import getFormId
from discordBot import shareResponsesMessage, sendDiscordMessage

if __name__ == "__main__":
    form_service = discovery.build("forms", "v1", credentials=credentials)
    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    formId = getFormId()
    if formId == "":
        exit()

    responses = form_service.forms().responses().list(formId=formId).execute()

    #drive_service.permissions().update(fileId=formId,permissionId="anyoneWithLink",body={'role':'writer'}).execute()


    #responses = responses['responses']
    #print("responses", responses)

    # if nobody submitted a response, do nothing
    if 'responses' not in responses or len(responses['responses']) == 0:
        sendDiscordMessage("Nobody submitted a response this month :(")
        exit()

    responses = responses['responses']
    print('responses', responses)

    # if didn't collect email addresses, share to everyone
    if 'respondentEmail' not in responses[0]:
        drive_service.permissions().update(
            fileId=formId,
            permissionId="anyoneWithLink",
            body={
                "role": "writer"
            }
        ).execute()

        print("added writer role for everyone")

    # if did collect email addresses, only share to people who submitted
    else:
        for response in responses:
            email = response['respondentEmail']
            print("adding", email)
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
