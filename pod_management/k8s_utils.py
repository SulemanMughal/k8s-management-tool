from my_site.utils import load_custom_kubeconfig
from kubernetes import client
from kubernetes.stream import portforward



def create_pod(namespace, pod_name, container_name, image, ports=None, env_vars=None):

    """

    Create a Pod in a specified namespace.

    """

    # config.load_kube_config()

    # v1 = client.CoreV1Api()

    core_api, _ = load_custom_kubeconfig()

    # Define the container

    container = client.V1Container(

        name=container_name,

        image=image,

        ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],

        env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],

    )

    # Define the Pod spec

    pod_spec = client.V1PodSpec(containers=[container])

    # Define the Pod

    pod = client.V1Pod(

        metadata=client.V1ObjectMeta(name=pod_name),

        spec=pod_spec,

    )

    try:

        response = core_api.create_namespaced_pod(namespace=namespace, body=pod)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        return {"status": "error", "error": str(e)}


def get_pod(namespace, pod_name):

    """

    Fetch details of a specific Pod.

    """

    # config.load_kube_config()
    core_api, _ = load_custom_kubeconfig()

    # v1 = client.CoreV1Api()

    try:

        response = core_api.read_namespaced_pod(name=pod_name, namespace=namespace)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        return {"status": "error", "error": str(e)}


def update_pod(namespace, pod_name, container_name, image, ports=None, env_vars=None):

    """

    Update an existing Pod by replacing its configuration.

    """

    core_api, _ = load_custom_kubeconfig()

    # v1 = client.CoreV1Api()

    # Define the updated container

    container = client.V1Container(

        name=container_name,

        image=image,

        ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],

        env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],

    )

    # Define the updated Pod spec

    pod_spec = client.V1PodSpec(containers=[container])

    # Define the updated Pod

    updated_pod = client.V1Pod(

        metadata=client.V1ObjectMeta(name=pod_name),

        spec=pod_spec,

    )

    try:

        response = core_api.replace_namespaced_pod(name=pod_name, namespace=namespace, body=updated_pod)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        return {"status": "error", "error": str(e)}


def delete_pod(namespace, pod_name):

    """

    Delete a Pod in a specified namespace.

    """

    # config.load_kube_config()
    # v1 = client.CoreV1Api()

    core_api, _ = load_custom_kubeconfig()

    try:

        response = core_api.delete_namespaced_pod(name=pod_name, namespace=namespace)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        return {"status": "error", "error": str(e)}




def list_pods(namespace=None):
    """
    List all pods in a specific namespace or all namespaces.
    """
    core_api, _ = load_custom_kubeconfig()

    try:
        if namespace:
            pods = core_api.list_namespaced_pod(namespace=namespace)
        else:
            pods = core_api.list_pod_for_all_namespaces()

        pod_list = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node_name": pod.spec.node_name,
                "containers": [
                    {
                        "name": container.name,
                        "image": container.image,
                    }
                    for container in pod.spec.containers
                ],
                "start_time": pod.status.start_time,
            }
            pod_list.append(pod_info)

        return {"status": "success", "pods": pod_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e)}



def port_forward_pod(namespace, pod_name, local_port, pod_port):
    """
    Port forward to a specific pod in a namespace.
    """
    core_api, _ = load_custom_kubeconfig()

    try:
        # Create a port-forward request
        pf = portforward(
            api_client=core_api.api_client,
            pod_name=pod_name,
            namespace=namespace,
            ports={local_port: pod_port},
        )

        return {
            "status": "success",
            "message": f"Port forwarding established: localhost:{local_port} -> {pod_name}:{pod_port}"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_pod_logs(namespace, pod_name, container_name=None, tail_lines=100):
    """
    Fetch logs of a specific pod.
    :param namespace: The namespace of the pod.
    :param pod_name: The name of the pod.
    :param container_name: Optional container name (if the pod has multiple containers).
    :param tail_lines: Number of lines to fetch from the logs (default: 100).
    :return: Pod logs as a string.
    """
    core_api, _ = load_custom_kubeconfig()

    try:
        logs = core_api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container_name,
            tail_lines=tail_lines,
        )
        return {"status": "success", "logs": logs}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e)}
