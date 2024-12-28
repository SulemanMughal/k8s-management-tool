from django.http import JsonResponse
from .k8s_utils import create_secret, get_secret, update_secret, delete_secret
from django.views.decorators.csrf import csrf_exempt
import json
import base64


@csrf_exempt
def create_secret_view(request):
    if request.method == "POST":
        # print(request.body)
        data = json.loads(request.body)
        # print(data)
        namespace = data.get("namespace", "default")
        secret_name = data.get("secret_name")
        secret_type = data.get("secret_type", "Opaque")
        secret_data = data.get("secret_data")

        if not secret_name or not secret_data:
            return JsonResponse({"error": "Secret name and data are required"}, status=400)
        secret_data = {key: base64.b64encode(value.encode()).decode() for key, value in (secret_data).items()}

        response = create_secret(namespace, secret_name, secret_type, secret_data)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"message": "Secret created successfully", "response": response["response"]})

def get_secret_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace", "default")
        secret_name = request.GET.get("secret_name")

        if not secret_name:
            return JsonResponse({"error": "Secret name is required"}, status=400)

        response = get_secret(namespace, secret_name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})


@csrf_exempt
def update_secret_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        secret_name = data.get("secret_name")
        secret_data = data.get("secret_data")

        if not secret_name or not secret_data:
            return JsonResponse({"error": "Secret name and data are required"}, status=400)

        
        secret_data = {key: base64.b64encode(value.encode()).decode() for key, value in (secret_data).items()}
        response = update_secret(namespace, secret_name, secret_data)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"message": "Secret updated successfully", "response": response["response"]})


@csrf_exempt
def delete_secret_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        secret_name = data.get("secret_name")

        if not secret_name:
            return JsonResponse({"error": "Secret name is required"}, status=400)

        response = delete_secret(namespace, secret_name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"message": response["response"]})
