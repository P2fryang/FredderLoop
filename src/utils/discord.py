"""Module containing Discord helper functions"""

import os

import requests

from src import config
from src.utils import database, services, masker


def send_discord_message(message: str) -> None:
    """Send a post to specified discord webhook"""
    if "FREDDERLOOP_PROD" in os.environ:
        requests.post(
            config.DISCORD_LETTERLOOP_WEBHOOK, timeout=30, json={"content": message}
        )
    else:
        masker.log(f"Discord message testing:\n{message}")


def create_form_message() -> None:
    """Send message with link to Fredderloop form"""
    docs_service = services.create_docs_service()
    form_id = database.get_form_id(docs_service=docs_service)
    message = (
        "New FredderLoop issue just dropped! 3 weeks (21th 00:00) to add questions here: "
        + f"https://docs.google.com/forms/d/{form_id}/edit"
        + "\n\nAlso, don't forget to set edit responses to true... "
        + "google form api currently doesn't support setting it in code"
    )
    send_discord_message(message)


def add_questions_reminder_message() -> None:
    """Send reminder to add questions"""
    docs_service = services.create_docs_service()
    form_id = database.get_form_id(docs_service=docs_service)
    message = (
        "Last day to add questions (due end of day)! "
        + f"https://docs.google.com/forms/d/{form_id}/edit"
    )
    send_discord_message(message)


def collect_responses_message() -> None:
    """Send message to submit answers"""
    docs_service = services.create_docs_service()
    form_id = database.get_form_id(docs_service=docs_service)
    message = (
        "Ready for responses here. Due in a week (28th 00:00): "
        + f"https://docs.google.com/forms/d/{form_id}/viewform"
        + "\n\n*Reminder: You'll only be able to see the newsletter if you submit a response*"
    )
    send_discord_message(message)


def submission_reminder_message() -> None:
    """Send reminder to submit answers"""
    docs_service = services.create_docs_service()
    form_id = database.get_form_id(docs_service=docs_service)
    message = (
        "@everyone \n"
        + "Last day to submit your answers, due end of day (there is NO auto-submit)! "
        + f"https://docs.google.com/forms/d/{form_id}/viewform"
    )
    send_discord_message(message)


def last_hour_reminder_message(names: list) -> None:
    """Send last hour reminder to submit answers"""
    if "FREDDERLOOP_PROD" not in os.environ:
        names = [f"{name[0]}***" for name in names]
    docs_service = services.create_docs_service()
    form_id = database.get_form_id(docs_service=docs_service)
    message = (
        f"{config.DISCORD_LETTERLOOP_ROLE} \n"
        + "Only ONE MORE HOUR to submit your answers (there is NO auto-submit)! "
        + f"https://docs.google.com/forms/d/{form_id}/viewform"
        + f"\n\nCurrent responses: {', '.join(names)}"
    )
    send_discord_message(message)


def share_responses_message(doc_id: str, need_to_add: list, err) -> None:
    """Send message with link to newsletter"""
    need_to_add_message = (
        f"\nNeed to share newsletter with these users: {', '.join(need_to_add)}"
    )
    if err:
        message = (
            "FredderLoop issue over!"
            + "\nNew FredderLoop starts on the 1st!"
            + "\n"
            + "But unforunately something failed...\n"
            + f"\nView newsletter here: https://docs.google.com/document/d/{doc_id}/edit"
            + need_to_add_message
        )
    else:
        message = (
            "FredderLoop issue over!"
            + "\nNew FredderLoop starts on the 1st!"
            + "\n"
            + f"\nView newsletter here: https://docs.google.com/document/d/{doc_id}/edit"
            + need_to_add_message
        )
    send_discord_message(message)

def share_responses_failed_message(err_str: str) -> None:
    """Send error message to dev channel"""
    if "FREDDERLOOP_PROD" in os.environ:
        requests.post(
            config.DISCORD_LETTERLOOP_WEBHOOK_DEV, timeout=30, json={"content": str(err_str)}
        )
    else:
        masker.log(f"Discord message testing:\n{err_str}")
    
