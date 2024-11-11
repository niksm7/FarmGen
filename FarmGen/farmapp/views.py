from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from farmapp.queryVectorData import queryDiseaseDetectionImage

def home(request):
    return render(request, "home.html")

def detectDisease(request):
    return render(request, "detectDisease.html")

@csrf_exempt
def uploadImageDisease(request):
    if request.method == "POST":
        file_data = request.FILES.get("diseaseFile")
        data_output = queryDiseaseDetectionImage(file_data)
        print(data_output)
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