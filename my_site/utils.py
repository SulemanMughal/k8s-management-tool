from kubernetes import client, config
from django.conf import settings

def load_custom_kubeconfig(config_path=settings.KUBE_CONFIG_PATH):
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
