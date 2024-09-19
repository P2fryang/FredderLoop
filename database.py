
def saveFormId(formId):
    with open("database", "w") as f:
        f.write(formId)

def getFormId():
    with open("database", "r") as f:
        return f.read()
