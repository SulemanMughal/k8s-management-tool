from django.http import JsonResponse


from .k8s_utils import list_all_namespaces, create_namespace, get_namespace_details,delete_namespace, update_namespace

from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

import traceback
import json


@csrf_exempt
@require_http_methods(['PATCH'])
def update_a_namespace_view(request):
    try:
        namespace_name = request.GET.get("namespace", None)
        metadata = json.loads(request.body)
        # print(metadata)
        if namespace_name:
            response = update_namespace(namespace_name, metadata)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        else:
            return JsonResponse({"error": "Namespace is required"}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)




@csrf_exempt
@require_http_methods(['DELETE'])
def delete_a_namespace_view(request):
    try:
        namespace_name = request.GET.get("namespace", None)
        if namespace_name:
            response = delete_namespace(namespace_name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        else:
            return JsonResponse({"error": "Namespace is required"}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    


def list_all_namespaces_view(reuqest):
    try:
        response = list_all_namespaces()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"images": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    

@csrf_exempt
@require_http_methods(['POST'])
def create_new_namespace_view(request):
    try:
        data = json.loads(request.body)
        namespace_name = data.get("name", None)
        if namespace_name:
            response = create_namespace(namespace_name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=400)
            return JsonResponse({"response": response["response"]})
        else:
            return JsonResponse({"error": "Namespace is required"}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    


@csrf_exempt
@require_http_methods(['GET'])
def namespace_detils_view(request):
    try:
        # data = json.loads(request.body)
        namespace_name = request.GET.get("namespace", None)
        # print(namespace_name)
        if namespace_name:
            response = get_namespace_details(namespace_name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        else:
            return JsonResponse({"error": "Namespace is required"}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    

