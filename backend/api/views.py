import firebase_admin
from django.shortcuts import render
from django.http import HttpResponse

import json
from firebase_admin import credentials
from firebase_admin import firestore,auth
from rest_framework import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pydoodle


cred = credentials.Certificate("C:/Users/kjaya/Desktop/OnlineComplier/backend/api/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app(cred)
db=firestore.client()
# fireBaseauth = firebase.auth()


@api_view(['GET'])
def run_code(request):

    code = """
a = int(input())
b = int(input())
 print(a+b,end="")
"""

    product = db.collection("coding")
    data = []
    docs = product.stream()
    c = pydoodle.Compiler(clientId="c3ee9988e3fdf5854e276a8264fb8f7a",
                          clientSecret="23dda9e96574603c738572d85f752a89dc9963e4588ab26d0221a8fa0073c5e4")

    for doc in docs:
        data.append(doc.to_dict())
    resultss = {}

    for i in data:
        for testcase, question in i.items():
            if (question == "sum of two numbers"):
                all_test = i["testcase"]
                for inputs in range(len(all_test)):
                    print(all_test[inputs])
                    testing=""
                    checking=[]
                    for i in all_test[inputs].keys():
                        if(i != 'output'):
                            checking.append(all_test[inputs][i])
                        else:
                            answer = all_test[inputs][i]
                    for discreteInp in checking:
                        testing+=f"{discreteInp}||"



                    result = c.execute(script=code, language="python3",
                                       stdIn=testing)  # Double pipe(||) is used to separate multiple inputs.

                    if(result.output[0] == answer):
                        resultss[inputs]=True
                    else:
                        resultss[inputs]=False

                print(resultss)

    return Response(resultss)

@api_view(['GET'])
def codingQuestionList(request):
    data = []
    codingQuestions = db.collection("coding")
    for doc in codingQuestions.stream():
        data.append(doc.to_dict())


    return Response(data)

@api_view(['GET'])
def getcodingQuestion(request,pk):
    print(pk,"ooooooooooooooooooooooooooooooooooooooo")
    datas = []
    codingQuestions = db.collection("coding")
    for doc in codingQuestions.stream():
        datas.append(doc.to_dict())
    data = None
    for i in datas:
        if i["qid"] == pk:
            data = i
            break


    return Response(data)

@api_view(['POST'])
def userCheck(request,pk):
    c = pydoodle.Compiler(clientId="c3ee9988e3fdf5854e276a8264fb8f7a",
                          clientSecret="23dda9e96574603c738572d85f752a89dc9963e4588ab26d0221a8fa0073c5e4")

    coding = request.data

    if(len(coding) > 1):
        check = coding["inputs"].split('\n')
        listToStr = '||'.join([str(elem) for elem in check])

        result = c.execute(script=coding['script'], language="python3",
                           stdIn=listToStr)
    else:
        result = c.execute(script=coding['script'], language="python3",)
    print(result.output[0])


    return Response(result.output[0])


@api_view(['POST'])
def run1stTestCase(request,pk):
    c = pydoodle.Compiler(clientId="c3ee9988e3fdf5854e276a8264fb8f7a",
                          clientSecret="23dda9e96574603c738572d85f752a89dc9963e4588ab26d0221a8fa0073c5e4")

    coding = request.data
    datas = []
    codingQuestions = db.collection("coding")
    for doc in codingQuestions.stream():
        datas.append(doc.to_dict())
    data = None
    for i in datas:
        if i["qid"] == pk:
            data = i
            break

    for fieldKey, fieldvalue in data.items():
        if fieldKey == 'testcase':
            testcases = fieldvalue
    testcaseList = []
    for key, value in testcases[0].items():
        if (key != "output"):
            testcaseList.append(value)

        else:
            output = value

    listToStr = '||'.join([str(elem) for elem in testcaseList])


    counts = coding['script'].count("input(")


    try:
        if(counts == len(testcaseList) ):
            result = c.execute(script=coding['script'], language="python3",
                           stdIn=listToStr)
            final = result.output[0]
        else:
            final = "you should must get inputs from user not direcetly declare"

    except Exception as e:
        print(e,"yyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        final = e

    try:
        if(int(final) == int(output)):
            final = f"{final}completed the program"
        else:
            final = "tescaseses are not match"
    except Exception as e:
        print(e,"999999999999999999999999999999999")



    return Response(final)


@api_view(['POST'])
def codeResult(request, pk):
    c = pydoodle.Compiler(clientId="c3ee9988e3fdf5854e276a8264fb8f7a",
                          clientSecret="23dda9e96574603c738572d85f752a89dc9963e4588ab26d0221a8fa0073c5e4")

    coding=request.data

    datas = []

    total={}

    codingQuestions = db.collection("coding")
    for doc in codingQuestions.stream():
        datas.append(doc.to_dict())
    data = None
    for i in datas:
        if i["qid"] == pk:
            data = i
            break

    for fieldKey, fieldvalue in data.items():
        if fieldKey == 'testcase':
            testcases = fieldvalue

    for singleTest in range(len(testcases)):
        testcaseList =[]
        for key, value in testcases[singleTest].items():
            if (key != "output"):
                testcaseList.append(value)
            else:
                output = value
        listToStr = '||'.join([str(elem) for elem in testcaseList])
        counts = coding['script'].count("input(")

        try:
            if (counts == len(testcaseList)):
                result = c.execute(script=coding['script'], language="python3",
                                   stdIn=listToStr)
                final = result.output[0]
            else:
                final = "you should must get inputs from user not direcetly declare"
                total.update({"error": final})

        except Exception as e:
            print(e, "yyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            final = e
            total.update({"error": final})


        if(final != "you should must get inputs from user not direcetly declare"):
            try:
                if (final.strip() == output.strip()):
                    final = f"{final}completed the program"
                    total.update({singleTest: final})
                else:
                    final = "tescaseses are not match"
                    total.update({singleTest: final})
            except Exception as e:
                print(e, "999999999999999999999999999999999")






    return Response(total)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    credent = data
    try:
        user = auth.create_user(email = credent['email'], password = credent['password'],display_name = credent['name'])

        # quizLevel = []
        # language=[]
        # for doc in db.collection("quiz").stream():
        #     quizLevel.append(doc.id)
        db.collection("newUsers").document(data['email']).set({
            "username": data['name'],
            "email" : data['email'],
            "uid":user.uid,


        })



        return Response({"username": data['name'],"email" : data['email']})
    except Exception as e:
        print(e,"ooooooooooooooooooooooooooooooooo")
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    data = request.data
    try:
        user = auth.get_user_by_email(data['email'])
        print(user.uid)


        result = {"username": user.display_name,"email" : user.email}
        return Response(result)
    except Exception as e:
        message = 'login failed'
        print(e)
        return Response(message ,status=status.HTTP_400_BAD_REQUEST)

# mcq
@api_view(['GET'])
def getMcqSubject(reguest):
    data = []
    mcqSub = db.collection("McqData")
    for doc in mcqSub.stream():
        data.append(doc.id)

    return Response(data)
@api_view(['GET'])
def getMcqQuestion(reguest,language,level):
#want to change the document name


    print(language,"languageeeeeeeeeeeeeee")
    print(level,"level")

    data = []
    mcqQuestions = db.collection("McqData").document(language).collection(level)
    for doc in mcqQuestions.stream():
        data.append(doc.to_dict())

    return Response(data)





@api_view(['GET'])
def getLevel(reguest,language):
    print(language,"language")
    data = []
    mcqLevels = db.collection("McqData")
    for doc in mcqLevels.stream():
        for collection_ref in doc.reference.collections():
            if(language == collection_ref.parent.path.split('/')[1]):
                data.append(collection_ref.id)


    return Response(data)
# Create your views here.

# Create your views here.
@api_view(['POST'])
def mcqSession(request,pk,bb):

    ddd={}

    data = request.data
    users = db.collection("newUsers")
    for doc in users.stream():
        ddd.update({doc.id:doc.to_dict()})




    for i in ddd:


        if(ddd[i]['email'] == data['email']):
            aa = db.collection("newUsers").document(i).collection(data['language']).document(data['level']).get()
            if aa.exists:
                userSession = {"question":data['question'],"userAnswer":data['userAnswer'],'level': data['level'],'language':data['language']}

                # print(data['question'] in aa.to_dict()['session'],"oooooooooooooooooooooooo")
                for test in aa.to_dict()['session']:
                    if(test['question']==data['question']):
                        print(test,"checkinggggggggggggggggg")
                        db.collection("newUsers").document(i).collection(data['language']).document(
                            data['level']).update(
                            {'session': firestore.ArrayRemove([test])})
                        break


                db.collection("newUsers").document(i).collection(data['language']).document(data['level']).update(
                {'session': firestore.ArrayUnion([userSession])})
            else:

                userSession = {"question":data['question'],"userAnswer":data['userAnswer'],'level': data['level'],'language':data['language']}
                db.collection("newUsers").document(i).collection(data['language']).add(
                {'session': firestore.ArrayUnion([userSession])}, data['level'])
            break

    return Response(data)


@api_view(['GET'])
def mcqSessionGet(request,language,level,email):
    data=[]



    sessionvalue={}


    users = db.collection("newUsers")
    for doc in users.stream():
        sessionvalue.update({doc.id:doc.to_dict()})

    for i in sessionvalue:
        if(sessionvalue[i]['email'] == email):

            data = db.collection("newUsers").document(email).collection(language).document(level).get()
            if(data.exists):
                print(data.to_dict()['session'])
                data =data.to_dict()["session"]
            else:
                data = []

    return Response(data)

@api_view(['GET'])
def getSpecifiedUser(reguest,email,language):
    data = []
    users = db.collection("newUsers").document(email).collection(language)
    for doc in users.stream():
        print(doc.id,"ooooooooooooo")
        data.append(doc.id)



    return Response(data)

