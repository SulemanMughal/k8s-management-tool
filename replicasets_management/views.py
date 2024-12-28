from django.http import JsonResponse
from .k8s_utils import create_replicaset_object, create_replicaset, list_replicasets, scale_replicaset



def list_replicasets_view(request, namespace):
    try:
        response = list_replicasets( namespace)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


