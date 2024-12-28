from my_site.utils import load_custom_kubeconfig
from kubernetes import client
from kubernetes.stream import portforward


def get_service_details(namespace, service_name):
    """
    Fetch details of a specific service in a namespace.
    :param namespace: The namespace of the service.
    :param service_name: The name of the service.
    :return: Service details or an error message.
    """
    core_api, _ = load_custom_kubeconfig()
    # v1 = client.CoreV1Api()

    try:
        # Fetch the service details
        service = core_api.read_namespaced_service(name=service_name, namespace=namespace)
        # print(service)
        # Prepare service details
        service_details = {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
            "cluster_ip": service.spec.cluster_i_ps,
            "external_ips": service.spec.external_i_ps,
            "ports": [
                {
                    "port": port.port,
                    "target_port": port.target_port,
                    "protocol": port.protocol,
                }
                for port in service.spec.ports
            ],
            "selector": service.spec.selector,
            "creation_timestamp": service.metadata.creation_timestamp,
            "labels": service.metadata.labels,
        }

        return {"status": "success", "service": service_details}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message
