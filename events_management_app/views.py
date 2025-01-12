from django.http import JsonResponse


from .k8s_utils import list_kubernetes_events, get_event_details

from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

import traceback
import json




@csrf_exempt
@require_http_methods(['GET'])
def get_event_details_view(request):
    try:
        namespace = request.GET.get("namespace", None)
        name = request.GET.get("name",  None)
        response = get_event_details(namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def list_events_view(request):
    try:
        response = list_kubernetes_events()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
