from django.http import JsonResponse
from .k8s_utils import get_node_metrics, get_pod_metrics



def get_node_metrics_view(request):
    if request.method == "GET":
        response = get_node_metrics()

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"nodes": response["nodes"]})





def get_pod_metrics_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace", None)  # Optional namespace filter
        response = get_pod_metrics(namespace)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"pods": response["pods"]})


