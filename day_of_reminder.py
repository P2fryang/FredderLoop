"""Send day of reminder to submit answers"""

import sys

from src.utils import database, discord, forms, services

if __name__ == "__main__":
    docs_service = services.create_docs_service()
    form_service = services.create_forms_service()

    form_id = database.get_form_id(docs_service=docs_service)
    if form_id == "":
        sys.exit()

    form = forms.get_form(form_service=form_service, form_id=form_id)
    nameQuestionId = form["items"][0]["questionItem"]["question"]["questionId"]

    responses = forms.get_form_responses(form_service=form_service, form_id=form_id)
    names = map(
        lambda x: x["answers"][nameQuestionId]["textAnswers"]["answers"][0]["value"],
        responses["responses"],
    )

    emails = [response.get("respondentEmail") for response in responses["responses"]]
    discord_ids = database.get_discord_ids(docs_service)
    list_of_shame = []

    for id, emails_list in discord_ids.items():
        found = False
        for email in emails:
            if email.lower() in emails_list:
                found = True
        if not found:
            list_of_shame.append(id)

    discord.day_of_reminder_message(list(names), list_of_shame)
