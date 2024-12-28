from django.http import JsonResponse
from .k8s_utils import create_deployment_object, create_deployment, get_deployment_status, update_deployment, delete_deployment
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_deployment_view(request, namespace):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        image = data.get("image")
        replicas = int(data.get("replicas", 1))
        labels = {"app": name}

        deployment = create_deployment_object(name, namespace, image, replicas, labels)
        try:
            response = create_deployment( namespace, deployment)
            # return JsonResponse({"message": f"Deployment {name} created."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



def monitor_deployment_view(request, namespace, name):
    try:
        response = get_deployment_status( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def update_deployment_view(request, ):
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace")
        name = data.get("name")
        container_name = data.get("container_name")
        new_image = data.get("new_image")

        try:
            response = update_deployment(namespace, name, container_name, new_image)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_deployment_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace")
        name = data.get("name")
        try:
            response = delete_deployment(namespace, name)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)