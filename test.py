import time
import json

def follow (thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def getUserCodeList (line: str) -> str:
    userCode = ""
    userCodeList = []
    object = line.split(' ')
    for obj in object:
        if "user" in obj:
            userCodeList.append(obj[5])
    userCode = ' '.join(userCodeList)
    return userCode

def analyze (line: str) -> None:
    outDict = dict()
    global selfCode
    attribute = str()
    user = str()
    with open("1.json", "a") as outFile:
        # self message
        if (line[0] != '<'):
            attribute = 'user'
            global selfCode
            user = selfCode
            content = line[:-1]
            outDict['content'] = content
        # announce
        elif (line[1] == 'a'):
            attribute = 'announce'
            if ("is connected" in line):
                outDict["type"] = "newConnected"
            elif ("already connected" in line):
                outDict["type"] = "alreadyConnected"
            elif ("is disconnected" in line):
                outDict["type"] = "disconnected"
            user = getUserCodeList(line)
        # other user message
        elif (line[1] == 'u'):
            user = line[5]
            attribute = 'user'
            content = line[8:-1]
            outDict['content'] = content
        outDict['attribute'] = attribute
        outDict['user'] = user 
        json.dump(outDict, outFile, indent=2)

def clearFile (fileName: str) -> None:
    open(fileName, "w").close()

selfCode = 0
if __name__ == '__main__':
    clearFile("1.json")
    first = 1
    with open("1.txt", "r") as logfile:
        titles = logfile.readlines()
        for title in titles:
            if first == 1:  # get self code
                selfCode = getUserCodeList(title)
                first = 0
            print(title)
            analyze(title)
        loglines = follow(logfile)
        for line in loglines:
            print(line)
            analyze(line)