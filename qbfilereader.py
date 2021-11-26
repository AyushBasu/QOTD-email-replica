import json
import datetime
import random
import os
import ast

QBFILE = "questionbank.json"
QIDSFILE = "questionids.txt"
usedqids = []

fo = open(QBFILE, "r")
qbank = fo.read()
fo.close()

dict_QIDCAT = {}
dict_Q = {}
dict_A = {}

x = json.loads(qbank)

todaysDate = datetime.datetime.now()
weekDayIndex = todaysDate.weekday()

questionArray = []

for dict in x:
    question = []
    for j in range(1):
        question.append(dict["_id"]["$oid"])
        question.append(dict["category"])
        question.append(dict["question"])
        question.append(dict["answer"])
    questionArray.append(question)
    dict_QIDCAT[dict["_id"]["$oid"]] = dict["category"]
    dict_Q[dict["_id"]["$oid"]] = dict["question"]
    dict_A[dict["_id"]["$oid"]] = dict["answer"]

answerDict = {}

answerList = list(dict_A.values())
newAnswerList = []
specialChars = '{}[]();":'

for answer in answerList:
    newAnswer = answer
    for character in answer:
        if character in specialChars:
            newAnswer = newAnswer.replace(character, "")
    newAnswerList.append(newAnswer)

for i in range(len(dict_A)):
    answerDict[list(dict_A.keys())[i]] = newAnswerList[i]

if weekDayIndex == 0:
    dailyCategoryList = ["Science"]
elif weekDayIndex == 1:
    dailyCategoryList = ["Literature"]
elif weekDayIndex == 2:
    dailyCategoryList = ["History", "Current Events", "Geography", "Mythology", "Philosophy", "Religion", "Social Science"]
elif weekDayIndex == 3:
    dailyCategoryList = ["Fine Arts"]
elif weekDayIndex == 4:
    dailyCategoryList = ["Trash"]
else:
    print("Not a weekday")
    quit()

moreQs = True
while moreQs:
    eligibleQuestions = []

    fo = open(QIDSFILE, "r")
    usedqids = fo.read().splitlines()
    fo.close()

    for q in questionArray:
        if q[1] in dailyCategoryList and q[0] not in usedqids:
            eligibleQuestions.append(q)

    if len(eligibleQuestions) == 0:
        fo = open("tempfile.txt", "w")
        i = 0

        for usedqid in usedqids:
            if dict_QIDCAT[usedqid] not in dailyCategoryList:
                fo.write(usedqid + "\n")
            i += 1
        fo.close()
        os.remove(QIDSFILE)
        os.rename("tempfile.txt", QIDSFILE)

    else:
        fo = open(QIDSFILE, "r")
        lines = fo.read().splitlines()
        fo.close()

        if len(lines) != 0:
            yesterdaysAnswerID = lines[-1]
            yesterdaysAnswer = dict_A[yesterdaysAnswerID]
            yesterdaysAnswer2 = answerDict[yesterdaysAnswerID]

        randomNumber = random.randint(0, len(eligibleQuestions) - 1)
        fo = open(QIDSFILE, "a")
        fo.write(eligibleQuestions[randomNumber][0] + "\n")
        fo.close()
        moreQs = False

todaysQuestion = dict_Q[eligibleQuestions[randomNumber][0]]

dailyEmail = "qbemailbody.txt"

fo = open(dailyEmail, "r")
emailContents = fo.read()
fo.close()

fo = open(QIDSFILE, "r")
lines = fo.read().splitlines()
fo.close()

if len(lines) != 1:
    emailContents = emailContents.replace("*ANSWER*", yesterdaysAnswer)
else:
    emailContents = emailContents.replace("*ANSWER*", "N/A")

emailContents = emailContents.replace("*QUESTION*", todaysQuestion)

fo = open("infodict.txt", "r")
infoDict = fo.read()
fo.close()

dictInfoDict = ast.literal_eval(infoDict)

correctReplierNames = []

if dictInfoDict != {}:
    for i in range(len(dictInfoDict)):
        if str(list(dictInfoDict.values())[i][2:]).lower() in yesterdaysAnswer2.lower():
            correctReplierNames.append(list(dictInfoDict.keys())[i][list(dictInfoDict.keys())[i].index(",")+2 : list(dictInfoDict.keys())[i].index("<")-2] + " " + list(dictInfoDict.keys())[i][1] + ".")
    if correctReplierNames != []:
        emailContents = emailContents.replace("*NAMES OF PEOPLE WHO ANSWERED RIGHT*", str(correctReplierNames))
    else:
        emailContents = emailContents.replace("*NAMES OF PEOPLE WHO ANSWERED RIGHT*", "N/A")
else:
    emailContents = emailContents.replace("*NAMES OF PEOPLE WHO ANSWERED RIGHT*", "N/A")

todaysCaption = "*TEST CAPTION*"
emailContents = emailContents.replace("*CUSTOM MESSAGE*", todaysCaption)


fo = open("finalemail.html", "w")
fo.write(emailContents)
fo.close()
