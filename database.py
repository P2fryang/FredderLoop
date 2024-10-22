import os

databaseDir = "./database"
formIdDir = databaseDir + "/formId"

def initDatabase():
    if not os.path.isdir("./database"):
        os.mkdir(databaseDir)

def saveFormId(formId):
    initDatabase()
    with open(formIdDir, "w") as f:
        f.write(formId)

def getFormId():
    initDatabase()
    with open(formIdDir, "r") as f:
        return f.read().strip()
