import constants
from database import getFormId
from services import create_service
from discordBot import lastHourReminderMessage

if __name__ == "__main__":
    form_service = create_service(constants.FORMS_SERVICE)

    formId = getFormId()
    if formId == "":
        exit()

    form = form_service.forms().get(formId=getFormId()).execute()
    nameQuestionId = form['items'][0]['questionItem']['question']['questionId']

    responses = form_service.forms().responses().list(formId=formId).execute()
    names = map(lambda x: x['answers'][nameQuestionId]['textAnswers']['answers'][0]['value'], responses['responses'])
    lastHourReminderMessage(list(names))

    
