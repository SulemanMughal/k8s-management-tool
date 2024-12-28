from django.shortcuts import render
from my_site.utils import load_custom_kubeconfig
from kubernetes import client
from django.http import JsonResponse

# Create your views here.
def index(request):
    template_name = "master_app/index.html"
    context = {

    }
    return render(request, template_name, context)


# List Nodes
def list_nodes(request):
    """
    List all Nodes in the cluster.
    """
    core_api, _ = load_custom_kubeconfig()
    try:
        nodes = core_api.list_node()
        return JsonResponse({"nodes": [{"name": node.metadata.name, "status": node.status.conditions[-1].type} for node in nodes.items]})
    except client.exceptions.ApiException as e:
        return JsonResponse({"error": str(e)}, status=500)
    


# Describe Node
def describe_node(request, node_name):
    """
    Get detailed information about a specific node.
    """
    core_api, _ = load_custom_kubeconfig()
    try:
        node = core_api.read_node(name=node_name)
        return JsonResponse({
            "name": node.metadata.name,
            "labels": node.metadata.labels,
            "annotations": node.metadata.annotations,
            "status": {
                "conditions": [
                    {"type": cond.type, "status": cond.status, "reason": cond.reason, "message": cond.message}
                    for cond in node.status.conditions
                ]
            }
        })
    except client.exceptions.ApiException as e:
        return JsonResponse({"error": str(e)}, status=500)
    


# Cordon Node
def cordon_node(request, node_name):
    """
    Cordon a node to prevent new Pods from being scheduled on it.
    """
    core_api, _ = load_custom_kubeconfig()
    try:
        patch_body = {"spec": {"unschedulable": True}}
        response = core_api.patch_node(name=node_name, body=patch_body)
        return JsonResponse(response.json())
    except client.exceptions.ApiException as e:
        return JsonResponse({"error": str(e)}, status=500)



# Uncordon Node
def uncordon_node(request, node_name):
    """
    Uncordon a node to allow new Pods to be scheduled on it.
    """
    core_api, _ = load_custom_kubeconfig()
    try:
        patch_body = {"spec": {"unschedulable": False}}
        response = core_api.patch_node(name=node_name, body=patch_body)
        return JsonResponse(response.json())
    except client.exceptions.ApiException as e:
        return JsonResponse({"error": str(e)}, status=500)



# Drain Node
def drain_node(request, node_name):
    """
    Drain a node by evicting all Pods except DaemonSet Pods.
    """
    core_api, _ = load_custom_kubeconfig()
    try:
        pods = core_api.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node_name}")
        for pod in pods.items:
            if "DaemonSet" not in [owner.kind for owner in (pod.metadata.owner_references or [])]:
                core_api.delete_namespaced_pod(name=pod.metadata.name, namespace=pod.metadata.namespace)
        return JsonResponse({"message": f"Node {node_name} drained successfully."})
    except client.exceptions.ApiException as e:
        return JsonResponse({"error": str(e)}, status=500)


