import pyrebase
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from farmapp.queryVectorData import queryDiseaseDetectionImage
from langchain_mongodb import MongoDBAtlasVectorSearch
from farmapp.intialize import *
from farmapp.promptsCollection import *
from farmapp.getLLMResponse import getBedrockResponseQA
from farmapp.pollyResponse import getPollyResponse
from farmapp.agentWorkflow import *
from .models import *


config = {
    "apiKey": "AIzaSyA4vWqjaseQxMVTEbGaxa9XiB76rtSJY5I",
    "authDomain": "farmgen-5ffbe.firebaseapp.com",
    "projectId": "farmgen-5ffbe",
    "storageBucket": "farmgen-5ffbe.firebasestorage.app",
    "messagingSenderId": "544211549084",
    "appId": "1:544211549084:web:893a8ef9608511058f6659",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()

def home(request):
    return render(request, "home.html")

def detectDisease(request):
    return render(request, "detectDisease.html")

@csrf_exempt
def uploadImageDisease(request):
    if request.method == "POST":
        file_data = request.FILES.get("diseaseFile")
        data_output = queryDiseaseDetectionImage(file_data)

        result_disease_count = {}
        result_type = "ProbableImages"
        for key in data_output:
            data = data_output[key]
            if not result_disease_count.get(data[1]):
                result_disease_count[data[1]] = []
            result_disease_count[data[1]].append(data[0])
            if len(result_disease_count[data[1]]) == 3:
                result_type = "Definite"
        if result_type == "Definite":
            return JsonResponse({"type": result_type, "result_disease": list(result_disease_count.keys())[0]})
        return JsonResponse({"type": result_type, "suggested_images": result_disease_count})

@csrf_exempt
def getBedrockResponse(request):
    if request.method == "POST":
        disease_name = request.POST.get("disease_name")
        disease_name = disease_name.replace("___", " ").replace("_", " ")
        disease_name = replaceNth(disease_name.lower(), disease_name.split(" ")[0].lower(), "", 2)
        disease_name = disease_name.replace("  ", " ")
        query = f"{disease_name} control cure"

        vectorStore = MongoDBAtlasVectorSearch(
            disease_cure_collection, embeddings_model_text, index_name=disease_cure_index
        )
        prompt = getPromptForDiseaseCure(given_language=request.session.get('language'))
        print("All good till here!")
        try:
            response = getBedrockResponseQA(query, vectorStore, prompt).replace("\n", "<br>")
            polly_response_filename = getPollyResponse(given_text=response, given_language=request.session.get('language'))
            return JsonResponse({"status": "Success", "response": response, "audio_filename": polly_response_filename})
        except Exception as e:
            print("Error: ", e)
            return JsonResponse({"status": "Error", "response": str(e)})

def chatBotDisplay(request):
    return render(request, "chatBot.html")

@csrf_exempt
def getChatbotResponse(request):
    if request.method == "POST":
        request_content = json.loads(request.body.decode('utf-8'))
        query = request_content.get("message")
        try:
            res = getAgentResponse(query, request.session.get('location_coors'))
            return JsonResponse({"status":"success", "response": res})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "response": "Sorry, I can't answer this qestion"})

def handleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            if authe.get_account_info(user['idToken'])['users'][0]["emailVerified"] is False:
                try:
                    authe.send_email_verification(user['idToken'])
                    message = "Please verify the email! Link has been sent!"
                except Exception:
                    message = "Please verify the email! Link has been sent!"
                return render(request, 'login.html', {"msg": message})

        except Exception:
            message = "Invalid Credentials"
            return render(request, 'login.html', {"msg": message})
        
        user = WebUser.objects.filter(id=request.session['uid'])[0]
        session_id = user['localId']
        request.session['email'] = email
        request.session['usrname'] = email.split("@")[0]
        request.session['uid'] = str(session_id)
        request.session['location_coors'] = user.location_coors
        request.session['language'] = user.language
    return render(request, 'login.html')

def handleSignUpUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        full_name = request.POST.get("fullname")
        password = request.POST.get("password")
        location = request.POST.get("location_coordinates")
        language = request.POST.get("language")
        new_user = authe.create_user_with_email_and_password(email, password)
        web_user = WebUser(id=new_user["localId"], full_name=full_name, location_coors=location, language=language)
        web_user.save()
    return HttpResponseRedirect(reverse("login"))

def handleLogout(request):
    if request.session.get('uid') is not None:
        auth.logout(request)
        authe.current_user = None
    return HttpResponseRedirect(reverse("home"))

def replaceNth(s, source, target, n):
    inds = [i for i in range(len(s) - len(source)+1) if s[i:i+len(source)]==source]
    if len(inds) < n:
        return  s
    s = list(s)
    s[inds[n-1]:inds[n-1]+len(source)] = target
    return ''.join(s)