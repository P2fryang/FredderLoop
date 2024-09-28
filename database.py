
def saveFormId(formId):
    with open("database/formId", "w") as f:
        f.write(formId)

def getFormId():
    with open("database/formId", "r") as f:
        return f.read()
