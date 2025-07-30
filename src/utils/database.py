"""Module containing database utility functions"""

# import os
import traceback

from src import config
from src.utils import docs, masker


def save_form_id(docs_service, form_id):
    """Save form id to specified document 'database'"""
    return push_to_database(docs_service=docs_service, content=f"form_id:{form_id}")


def push_to_database(docs_service, content):
    """Helper function appending to specified document 'database'"""
    insert_index = docs.get_last_insert_index(
        docs_service=docs_service, file_id=config.DOC_ID_DOCUMENT_ID
    )
    request, _ = docs.add_paragraph(content, insert_index)
    err = docs.batch_update(docs_service, config.DOC_ID_DOCUMENT_ID, request)
    if err:
        masker.log(
            " ".join(
                map(str, traceback.format_exception(type(err), err, err.__traceback__))
            )
        )


def get_form_id(docs_service):
    """Helper function pulling last form id from specified document 'database'"""
    form_id = (
        docs.search_latest_text_lower(
            docs_service=docs_service,
            file_id=config.DOC_ID_DOCUMENT_ID,
            search_string="form_id",
        )
        .split(":")[-1]
        .strip()
    )
    if "" == form_id:
        raise KeyError("form id not found in database")
    return form_id


def get_discord_ids(docs_service):
    """Helper function pulling discord ids from specified document 'database'"""
    document = docs.get_document(docs_service, config.DISCORD_ID_DOCUMENT_ID)["body"]["content"]
    discord_ids = {}
    """
    expect the doc to be formatted such as:
    <name>: <discord id> <email> <email> ...
    """
    for p in reversed(document):
        try:
            if "paragraph" not in p:
                continue
            paragraph_element = p["paragraph"]["elements"][-1]
            paragraph_text_content = paragraph_element["textRun"]["content"].strip()
            if ": " in paragraph_text_content.lower():
                stuff = paragraph_text_content.split(" ")
                stuff2 = [x.lower() for x in stuff]
                # probably unecessary...
                stuff2[1] = stuff[1]
                # stuff[0] = "<name>:"
                # stuff[1] = "<discord id>"
                # stuff[2+] = "<email>"
                discord_ids[stuff[1]] = stuff2[2:]
        except Exception as e:
            # no text found, might be table? Ignoring...
            masker.log(
                " ".join(
                    map(str, traceback.format_exception(type(e), e, e.__traceback__))
                )
            )
            masker.log("Not basic text, ignoring...")
    return discord_ids
