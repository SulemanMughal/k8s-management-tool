from my_site.utils import load_custom_kubeconfig
from kubernetes import client
# import json


def list_kubernetes_events():
    """
    List all events available in Kubernetes.
    """
    core_api, _ = load_custom_kubeconfig()
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