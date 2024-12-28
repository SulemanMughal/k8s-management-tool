from my_site.utils import load_custom_kubeconfig
from kubernetes import client


def create_secret(namespace, secret_name, secret_type, secret_data):
    """
    Create a Kubernetes Secret.
    :param namespace: Namespace for the Secret.
    :param secret_name: Name of the Secret.
    :param secret_type: Type of the Secret (e.g., kubernetes.io/tls).
    :param secret_data: Dictionary of base64-encoded data.
    :return: Status of Secret creation.
    """
    core_api, _ = load_custom_kubeconfig()
    # v1 = client.CoreV1Api()

    secret = client.V1Secret(
        metadata=client.V1ObjectMeta(name=secret_name),
        type=secret_type,
        data=secret_data,
    )

    print(secret)

    try:
        response = core_api.create_namespaced_secret(namespace=namespace, body=secret)

        print(response)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # print(e)
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



def get_secret(namespace, secret_name):
    """
    Retrieve a Kubernetes Secret.
    :param namespace: Namespace of the Secret.
    :param secret_name: Name of the Secret.
    :return: Secret details or error message.
    """
    core_api, _ = load_custom_kubeconfig()
    # v1 = client.CoreV1Api()

    try:
        secret = core_api.read_namespaced_secret(name=secret_name, namespace=namespace)
        return {"status": "success", "response": secret.to_dict()}
    except client.exceptions.ApiException as e:
        
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



def update_secret(namespace, secret_name, secret_data):
    """
    Update a Kubernetes Secret.
    :param namespace: Namespace of the Secret.
    :param secret_name: Name of the Secret.
    :param secret_data: Dictionary of base64-encoded data to update.
    :return: Status of Secret update.
    """
    core_api, _ = load_custom_kubeconfig()
    # v1 = client.CoreV1Api()

    try:
        existing_secret = core_api.read_namespaced_secret(name=secret_name, namespace=namespace)
        existing_secret.data = secret_data
        response = core_api.replace_namespaced_secret(name=secret_name, namespace=namespace, body=existing_secret)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



def delete_secret(namespace, secret_name):
    """
    Delete a Kubernetes Secret.
    :param namespace: Namespace of the Secret.
    :param secret_name: Name of the Secret.
    :return: Status of Secret deletion.
    """
    core_api, _ = load_custom_kubeconfig()
    # v1 = client.CoreV1Api()

    try:
        response = core_api.delete_namespaced_secret(name=secret_name, namespace=namespace)
        return {"status": "success", "response": "Secret deleted successfully"}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message
