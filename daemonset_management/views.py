# from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from .k8s_utils import create_daemonset, describe_daemonset, list_daemonsets, update_daemonset_image, delete_daemonset, get_pods_managed_by_daemonsets, get_pods_managed_by_specific_daemonset, update_daemonset_node_selector, update_daemonset_node_affinity,pause_daemonset,resume_daemonset, get_nodes_for_daemonset, change_daemonset_namespace, daemonset_rollout_status,daemonset_rollout_status_periodic, get_daemonset_events,update_rollout_history, get_rollout_history
import json

@csrf_exempt
def create_daemonset_view(request):
    """
    Django view to create a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    # try:
    #     response = create_daemonset( namespace)
    #     return JsonResponse({"message": f"DaemonSet created: {response.metadata.name}"})
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=500)

    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        objLabels = data.get("objLabels")
        matchLabels = data.get("matchLabels")
        templateLabels = data.get("templateLabels")
        containerName = data.get("containerName")
        containerImage = data.get("containerImage")


        # deployment = create_daemonset(name, namespace, image, replicas, labels)
        try:
            response = create_daemonset( namespace, objName, objLabels, matchLabels, templateLabels, containerName, containerImage)
            # return JsonResponse({"message": f"Deployment {name} created."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def describe_daemonset_view(request):
    """
    Django view to describe a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "GET":
        # data = json.loads(request.body)
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = describe_daemonset( namespace, name)
            # return JsonResponse(response)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)




def list_daemonsets_view(request):
    """
    Django view to list all DaemonSets.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "GET":
        # data = json.loads(request.body)
        namespace = request.GET.get("namespace")
        try:
            response = list_daemonsets( namespace)
            # return JsonResponse(response)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:

            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def update_daemonset_image_view(request):
    """
    Django view to update the image of a DaemonSet's container.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        containerName = data.get("containerName")
        newContainerImage = data.get("newContainerImage")
        try:
            response = update_daemonset_image( namespace, objName, containerName, newContainerImage)
            # return JsonResponse({"message": f"Deployment {name} updated."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    



@csrf_exempt
def delete_daemonset_view(request):
    """
    Django view to delete a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        name = data.get("name")
        try:
            response = delete_daemonset( namespace, name)
            # return JsonResponse({"message": f"Deployment {name} deleted."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def get_pods_managed_by_daemonsets_view(request):
    """
    Django view to get pods managed by DaemonSets.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "GET":
        # data = json.loads(request.body)
        namespace = request.GET.get("namespace")
        try:
            response = get_pods_managed_by_daemonsets( namespace)
            # return JsonResponse(response)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def get_pods_managed_by_specific_daemonset_view(request):
    """
    Django view to get pods managed by a specific DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "GET":
        # data = json.loads(request.body)
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = get_pods_managed_by_specific_daemonset( namespace, name)
            # return JsonResponse(response)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def update_daemonset_node_selector_view(request):
    """
    Django view to update the node selector of a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        nodeSelector = data.get("nodeSelector")
        try:
            response = update_daemonset_node_selector( namespace, objName, nodeSelector)
            # return JsonResponse({"message": f"Deployment {name} updated."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def update_daemonset_node_affinity_view(request):
    """
    Django view to update the node affinity of a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        nodeAffinity = data.get("nodeAffinity")
        try:
            response = update_daemonset_node_affinity( namespace, objName, nodeAffinity)
            # return JsonResponse({"message": f"Deployment {name} updated."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
@csrf_exempt
def pause_daemonset_view(request):
    """
    Django view to pause a DaemonSet.
    """
    # api_instance = load_kubernetes_config()
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        try:
            response = pause_daemonset( namespace, objName)
            # return JsonResponse({"message": f"Deployment {name} updated."})
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def resume_daemonset_view(request):
    """
    Django view to resume a DaemonSet.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        node_selector=data.get("node_selector")
        try:
            response = resume_daemonset( namespace, objName,node_selector)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def get_nodes_for_daemonset_view(request):
    """
    Django view to get nodes for a DaemonSet.
    """
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        objName = request.GET.get("name")
        try:
            response = get_nodes_for_daemonset(namespace, objName)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def change_daemonset_namespace_view(request):
    """
    Django view to change the namespace of a DaemonSet.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        newNamespace = data.get("newNamespace")
        try:
            response = change_daemonset_namespace( namespace, objName, newNamespace)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def daemonset_rollout_status_view(request):
    """
    Django view to get the rollout status of a DaemonSet.
    """
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = daemonset_rollout_status(namespace, name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def daemonset_rollout_status_periodic_view(request):
    """
    Django view to get the rollout status of a DaemonSet periodically.
    """
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = daemonset_rollout_status_periodic(namespace, name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def get_daemonset_events_view(request):
    """
    Django view to get events of a DaemonSet.
    """
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = get_daemonset_events(namespace, name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def update_rollout_history_view(request):
    """
    Django view to update the rollout history of a DaemonSet.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        objName = data.get("name")
        newRolloutHistory = data.get("newRolloutHistory")
        try:
            response = update_rollout_history(namespace, objName, newRolloutHistory)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
def get_rollout_history_view(request):
    """
    Django view to get the rollout history of a DaemonSet.
    """
    if request.method == "GET":
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        try:
            response = get_rollout_history(namespace, name)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=response["error-status"])
            return JsonResponse({"response": response["response"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)