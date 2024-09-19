from datetime import datetime

def getDefaultFormHead():
    date = datetime.today().strftime('%Y-%m-%d')
    return {
        "info": {
            "title": date + " LetterLoop Questions",
            "documentTitle": date
        }
    }


defaultFormBody = {
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
