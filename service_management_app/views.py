from django.http import JsonResponse
from .k8s_utils import get_service_details



def get_service_details_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        service_name = request.GET.get("service_name")

        if not namespace or not service_name:
            return JsonResponse({"error": "Namespace and service name are required"}, status=400)

        response = get_service_details(namespace, service_name)
        # print(response)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        
        return JsonResponse({"service": response["service"]})
