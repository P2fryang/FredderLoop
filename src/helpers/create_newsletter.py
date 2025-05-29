"""Contains helper function to create newsletter"""

import datetime

from src.utils import database, docs, forms, masker, services


def create_newsletter(form: dict, responses: dict) -> tuple[str, dict]:
    """Creates newsletter from form response"""
    docs_service = services.create_docs_service()

    doc = docs.create_document(
        docs_service=docs_service,
        title=f"{datetime.datetime.now().strftime('%Y-%m')} Gletterloop Newsletter",
    )
    doc_id = doc["documentId"]
    # save newsletter ID
    database.push_to_database(
        docs_service=docs_service, content=f"newsletterID:{doc_id}"
    )
    current_index = 1
    processed, email_mapping, no_photos = forms.process_responses(form, responses)
    photo_ans = []
    requests = []

    # add title
    title = f"Gletterloop for {datetime.datetime.now().strftime('%B %Y')}"
    tmp, current_index = docs.add_title(title, current_index)
    requests.extend(tmp)

    # add horizontal bar (with thin table with top border line, google api no horizontal rule)
    tmp, current_index = docs.add_horizontal_rule(current_index)
    requests.extend(tmp)

    if not no_photos:
        photo_ans = processed.pop()
    # add each question besides photo (pop photo into diff var)
    for response in processed:
        tmp, current_index = docs.add_response(response, current_index)
        requests.extend(tmp)

    # add photos
    if photo_ans:
        tmp, current_index = docs.add_photos(photo_ans, current_index)
        requests.extend(tmp)

    # update font
    tmp, _ = docs.update_font(curr_ind=current_index)
    requests.extend(tmp)

    # use for debugging only
    # with open("failed.py", "w+") as f:
    #     masker.log("Writing requests to failed.py")
    #     nreqs = {}
    #     i = 0
    #     for req in requests:
    #         nreqs[i] = req
    #         i += 1
    #     f.write(str(nreqs))

    # push changes
    docs.batch_update(docs_service=docs_service, file_id=doc_id, requests=requests)

    return doc_id, email_mapping
