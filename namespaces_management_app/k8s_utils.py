from my_site.utils import load_custom_kubeconfig
from kubernetes import client
import json



def list_all_namespaces():
    """
    List all namespaces available in Kubernetes.
    """
    core_api,_ = load_custom_kubeconfig()
    try:
        namespaces = core_api.list_namespace().items
        namespace_list = [ns.metadata.name for ns in namespaces]
        return {"status": "success", "response": namespace_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def create_namespace(namespace_name):
    """
    Create a new namespace in Kubernetes.
    """
    core_api,_ = load_custom_kubeconfig()
    namespace = client.V1Namespace(
        metadata=client.V1ObjectMeta(name=namespace_name)
    )
    try:
        response = core_api.create_namespace(body=namespace)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def get_namespace_details(namespace_name):
    """
    Get details of a specific namespace in Kubernetes.
    """
    core_api,_ = load_custom_kubeconfig()
    try:
        namespace = core_api.read_namespace(name=namespace_name)
        return {"status": "success", "response": namespace.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def delete_namespace(namespace_name):
    """
    Delete a namespace in Kubernetes.
    """
    core_api,_ = load_custom_kubeconfig()
    try:
        response = core_api.delete_namespace(name=namespace_name, body=client.V1DeleteOptions())
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def update_namespace(namespace_name, new_metadata):
    """
    Update a namespace in Kubernetes.
    """
    core_api,_ = load_custom_kubeconfig()
    try:
        patch_body = {
            "metadata": new_metadata
        }
        response = core_api.patch_namespace(name=namespace_name, body=patch_body)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}