from django.http import JsonResponse
from .k8s_utils import  create_replicaset, list_replicasets, scale_replicaset, update_replicaset, get_replicaset_status, delete_replicaset, get_replicaset_pods, get_replicaset_events, get_replicaset_logs, delete_replicaset_orphan
from django.views.decorators.csrf import csrf_exempt
import json

def list_replicasets_view(request, namespace):
    try:
        response = list_replicasets( namespace)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def create_replicaset_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        replicaName = data.get("name")
        namespace = data.get("namespace")
        labels = data.get("labels")
        replicas = int(data.get("replicas", 1))
        match_labels = data.get("match_labels")
        container_name = data.get("containerName")
        container_image = data.get("containerImage")
        container_port = int(data.get("containerPort", 80))
        response = create_replicaset( namespace, replicaName, labels, replicas, match_labels, container_name, container_image, container_port)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def update_replicate_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        replicaName = data.get("name")
        namespace = data.get("namespace")
        replicas = int(data.get("replicas", 1))
        response = update_replicaset( namespace, replicaName, replicas)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_replicate_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = get_replicaset_status( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_replicate_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = delete_replicaset( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_replicate_pods_view(request):
    try:
        namespace = request.GET.get("namespace")
        labels = request.GET.get("labels")
        response = get_replicaset_pods( namespace, labels)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_replicate_events_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = get_replicaset_events( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_replicate_logs_view(request):
    try:
        namespace = request.GET.get("namespace")
        pod_name = request.GET.get("pod_name")
        container_name = request.GET.get("container_name")
        response = get_replicaset_logs( namespace, pod_name, container_name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def delete_replicate_orphan_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = delete_replicaset_orphan( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)