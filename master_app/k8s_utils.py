from my_site.utils import load_custom_kubeconfig
from kubernetes import client
from kubernetes.stream import portforward



def get_node_pod_cidr(node_name):

    """

    Fetch the podCIDR for a specific node.

    :param node_name: The name of the node.

    :return: podCIDR of the node or error message.

    """

    core_api, _ = load_custom_kubeconfig()

    # v1 = client.CoreV1Api()

    try:

        # Fetch the node details

        node = core_api.read_node(name=node_name)

        pod_cidr = node.spec.pod_cidr  # Extract the podCIDR

        return {"status": "success", "podCIDR": pod_cidr}

    except client.exceptions.ApiException as e:

        return {"status": "error", "error": str(e)}
