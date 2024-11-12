from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from farmapp.queryVectorData import queryDiseaseDetectionImage
from langchain_mongodb import MongoDBAtlasVectorSearch
from farmapp.intialize import *
from farmapp.promptsCollection import *
from farmapp.getLLMResponse import getBedrockResponseQA
from farmapp.pollyResponse import getPollyResponse


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
        prompt = getPromptForDiseaseCure(given_language="English")
        print("All good till here!")
        try:
            response = getBedrockResponseQA(query, vectorStore, prompt).replace("\n", "<br>")
            polly_response_filename = getPollyResponse(given_text=response)
            return JsonResponse({"status": "Success", "response": response, "audio_filename": polly_response_filename})
        except Exception as e:
            print("Error: ", e)
            return JsonResponse({"status": "Error", "response": str(e)})


def replaceNth(s, source, target, n):
    inds = [i for i in range(len(s) - len(source)+1) if s[i:i+len(source)]==source]
    if len(inds) < n:
        return  s
    s = list(s)
    s[inds[n-1]:inds[n-1]+len(source)] = target
    return ''.join(s)