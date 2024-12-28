import decouple
from kubernetes import client, config


def load_custom_kubeconfig(config_path):
    """
    Load a user-defined kubeconfig for the Kubernetes API client.
    :param config_path: Path to the kubeconfig file.
    """
    try:
        # Load the kubeconfig file from the specified path
        config.load_kube_config(config_file=config_path)
        # Return the API instance for core and apps
        core_api = client.CoreV1Api()
        apps_api = client.AppsV1Api()
        return core_api, apps_api
    except Exception as e:
        raise Exception(f"Error loading custom kubeconfig: {e}")


def list_pods_with_custom_config(config_path):
    """
    List all Pods in the cluster using a custom kubeconfig.
    """
    core_api, _ = load_custom_kubeconfig(config_path)
    try:
        pods = core_api.list_pod_for_all_namespaces()
        print([{"name": pod.metadata.name, "namespace": pod.metadata.namespace} for pod in pods.items])
    except client.exceptions.ApiException as e:
        raise Exception(f"Error listing Pods: {e}")


list_pods_with_custom_config(decouple.config("KUBE_CONFIG_PATH"))