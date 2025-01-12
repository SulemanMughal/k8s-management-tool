from my_site.utils import load_custom_kubeconfig
from kubernetes import client
# import json


def list_kubernetes_events():
    """
    List all events available in Kubernetes.
    """
    core_api, _ ,_, _= load_custom_kubeconfig()
    try:
        events = core_api.list_event_for_all_namespaces().items
        event_list = [
            {
                "namespace": event.metadata.namespace,
                "name": event.metadata.name,
                "reason": event.reason,
                "message": event.message,
                "type": event.type,
                "timestamp": event.last_timestamp
            }
            for event in events
        ]
        return {"status": "success", "response": event_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def get_event_details(namespace, name):
    """
    Get details of a specific event in Kubernetes.
    """
    core_api, _ , _, _= load_custom_kubeconfig()
    try:
        event = core_api.read_namespaced_event(name=name, namespace=namespace)
        event_details = {
            "namespace": event.metadata.namespace,
            "name": event.metadata.name,
            "reason": event.reason,
            "message": event.message,
            "type": event.type,
            "timestamp": event.last_timestamp,
            "involved_object": {
                "kind": event.involved_object.kind,
                "name": event.involved_object.name,
                "namespace": event.involved_object.namespace,
                "uid": event.involved_object.uid
            }
        }
        return {"status": "success", "response": event_details}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}