import json

def loadbutter():
    file = open('butter.json')
    filedata = json.load(file)
    return filedata

def savebutter(data):
    with open('butter.json', 'w') as file:
        json.dump(data, file, indent=4)