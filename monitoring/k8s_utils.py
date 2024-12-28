from my_site.utils import load_custom_kubeconfig
from kubernetes import client
from kubernetes.stream import portforward





def get_node_metrics():
    """
    Fetch resource usage metrics for all nodes.
    Equivalent to `kubectl top nodes`.
    """
    core_api, _ = load_custom_kubeconfig()
    custom_api = client.CustomObjectsApi()

    try:
        # Fetch metrics for nodes
        metrics = custom_api.list_cluster_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            plural="nodes"
        )

        node_metrics = [
            {
                "name": item["metadata"]["name"],
                "cpu": item["usage"]["cpu"],
                "memory": item["usage"]["memory"]
            }
            for item in metrics.get("items", [])
        ]

        return {"status": "success", "nodes": node_metrics}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e)}



def get_pod_metrics(namespace=None):
    """
    Fetch resource usage metrics for all pods in a namespace or all namespaces.
    Equivalent to `kubectl top pods` or `kubectl top pods -n <namespace>`.
    """
    core_api, _ = load_custom_kubeconfig()
    custom_api = client.CustomObjectsApi()

    try:
        if namespace:
            metrics = custom_api.list_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=namespace,
                plural="pods"
            )
        else:
            metrics = custom_api.list_cluster_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                plural="pods"
            )

        pod_metrics = [
            {
                "namespace": item["metadata"]["namespace"],
                "name": item["metadata"]["name"],
                "containers": [
                    {
                        "name": container["name"],
                        "cpu": container["usage"]["cpu"],
                        "memory": container["usage"]["memory"]
                    }
                    for container in item["containers"]
                ]
            }
            for item in metrics.get("items", [])
        ]

        return {"status": "success", "pods": pod_metrics}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e)}




