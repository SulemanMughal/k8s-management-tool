from django.http import JsonResponse


from .k8s_utils import list_all_network_policies,create_network_policy, list_all_ip_pools, create_ip_pool, get_ip_pool_details, update_ip_pool, delete_ip_pool, monitor_ip_pool_usage, get_ip_pool_metrics, assign_ip_pool_to_pod, assign_ip_pool_to_namespace

from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

import traceback
import json


@csrf_exempt
@require_http_methods(['POST'])
def assign_ip_pool_view(request):
    try:
        data = json.loads(request.body)
        # response = assign_ip_pool_to_pod(data)
        namespace = data.get("namespace")
        pod_name = data.get("pod_name")
        ip_pool_name = data.get("ip_pool_name")

        # Check if all required fields are present
        if not namespace or not ip_pool_name:
            return JsonResponse({"error": "namespace and ip_pool_name are required fields"}, status=400)

        # Assign IP Pool to namespace or pod
        if pod_name:
            response = assign_ip_pool_to_pod(namespace, pod_name, ip_pool_name)
        else:
            response = assign_ip_pool_to_namespace(namespace, ip_pool_name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def get_ip_pool_metrics_view(request):
    try:
        
        response = get_ip_pool_metrics()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(['GET'])
def monitor_ip_pool_usage_view(request):
    try:
        
        response = monitor_ip_pool_usage()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
@require_http_methods(['DELETE'])
def delete_ip_pool_view(request):
    try:
        name = request.GET.get("name", None)

        # Check if all required fields are present
        if not name :
            return JsonResponse({"error": "name is required."}, status=400)
        
        response = delete_ip_pool(name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(['PUT'])
def update_ip_pool_view(request):
    try:
        # name = request.GET.get("name", None)
        data = json.loads(request.body)
        # Extract fields from the request body
        name = data.get("name")
        updates = data.get("updates")

        # Check if all required fields are present
        if not name or not updates :
            return JsonResponse({"error": "name and updates fields are required."}, status=400)
        
        response = update_ip_pool(name, updates)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def get_ip_pool_details_view(request):
    try:
        name = request.GET.get("name", None)

        # Check if all required fields are present
        if not name :
            return JsonResponse({"error": "name is required."}, status=400)
        
        response = get_ip_pool_details(name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def create_ip_pool_view(request):
    try:
        data = json.loads(request.body)
        # Extract fields from the request body
        name = data.get("name")
        cidr = data.get("cidr")
        ipip_mode = data.get("ipip_mode", "Always")
        vxlan_mode = data.get("vxlan_mode", "Never")
        nat_outgoing = data.get("nat_outgoing", True)

        # Check if all required fields are present
        if not name or not cidr:
            return JsonResponse({"error": "name and cidr are required fields"}, status=400)
        
        response = create_ip_pool(name, cidr, ipip_mode, vxlan_mode, nat_outgoing)
        # print(response)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def list_all_ip_pools_view(request):
    try:
        response = list_all_ip_pools()
        # print(response)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(['POST'])
def create_network_policy_view(request):
    try:
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        policy_name = data.get("policy_name")
        pod_selector = data.get("pod_selector")
        policy_types = data.get("policy_types")
        match_labels = data.get("match_labels")
        # Check if all required parameters are present
        if not policy_name or not pod_selector or not policy_types or not match_labels:
            return JsonResponse({"error": "policy_name, pod_selector, policy_types, and match_labels are required"}, status=400)
        response = create_network_policy(namespace, policy_name, pod_selector, policy_types,match_labels)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)



# @csrf_exempt
@require_http_methods(['GET'])
def list_network_policies_view(request):
    try:
        response = list_all_network_policies()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

