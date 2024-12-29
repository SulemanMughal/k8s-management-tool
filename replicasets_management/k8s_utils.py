from my_site.utils import load_custom_kubeconfig
from kubernetes import client


# Designing ReplicaSets
def create_replicaset_object(replicaName, labels, replicas, match_labels, container_name, container_image, container_port):
    return client.V1ReplicaSet(
        metadata=client.V1ObjectMeta(name=replicaName, labels=labels),
        spec=client.V1ReplicaSetSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels=match_labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name=container_name,
                        image=container_image,
                        ports=[client.V1ContainerPort(container_port=container_port)]
                    )
                ])
            )
        )
    )


# Creating ReplicaSets
def create_replicaset( namespace,  replicaName, labels, replicas, match_labels, container_name, container_image, container_port):
    core_api, apps_api = load_custom_kubeconfig()
    replicaset = create_replicaset_object(replicaName, labels, replicas, match_labels, container_name, container_image, container_port)
    try:
        response = apps_api.create_namespaced_replica_set(
            namespace=namespace,
            body=replicaset
        )
        # print(f"ReplicaSet created: {response.metadata.name}")
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


# Inspecting ReplicaSets
def list_replicasets( namespace):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.list_namespaced_replica_set(namespace)
        # for rs in api_response.items:
        #     print(f"Name: {rs.metadata.name}, Replicas: {rs.status.replicas}")
        # return api_response.items
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


# Updating ReplicaSets
def update_replicaset( namespace, name, replicas):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        patch_body = {
            "spec": {
                "replicas": replicas
            }
        }
        response = apps_api.patch_namespaced_replica_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


# Scaling ReplicaSets
def scale_replicaset( namespace, name, replicas):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        scale_body = {"spec": {"replicas": replicas}}
        response = apps_api.patch_namespaced_replica_set_scale(
            name=name,
            namespace=namespace,
            body=scale_body
        )
        # print(f"Scaled ReplicaSet {name} to {replicas} replicas.")
        # return api_response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # print(f"Exception when scaling ReplicaSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


# Get ReplicaSet Status
def get_replicaset_status( namespace, name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.read_namespaced_replica_set_status(
            name=name,
            namespace=namespace
        )
        status = {
            "name": response.metadata.name,
            "replicas": response.status.replicas,
            "ready_replicas": response.status.ready_replicas,
            "available_replicas": response.status.available_replicas,
            "selector": response.spec.selector.match_labels,
            "containers": [{
                "name": c.name,
                "image": c.image
            } for c in response.spec.template.spec.containers]

        }
        # return status
        return {"status": "success", "response": status}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



# Delete ReplicaSet
def delete_replicaset( namespace, name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.delete_namespaced_replica_set(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions()
        )
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error deleting ReplicaSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


def get_replicaset_pods( namespace, label_selector):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
        # return [{"name": pod.metadata.name, "status": pod.status.phase} for pod in pods.items]
        return {"status": "success", "response": [{"name": pod.metadata.name, "status": pod.status.phase} for pod in pods.items]}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error getting Pods for ReplicaSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


def get_replicaset_events(namespace, name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        field_selector = f"involvedObject.name={name},involvedObject.kind=ReplicaSet"
        events = core_api.list_namespaced_event(namespace=namespace, field_selector=field_selector)
        # print(events.items)
        # return [{"message": event.message, "timestamp": event.last_timestamp} for event in events.items]
        return {"status": "success", "response": [{"message": event.message, "timestamp": event.last_timestamp} for event in events.items]}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



def get_replicaset_logs(namespace, pod_name, container_name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        logs = core_api.read_namespaced_pod_log(
            name=pod_name, namespace=namespace, container=container_name
        )
        # return logs
        return {"status": "success", "response": logs}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



# Deletion with --cascade=orphan
def delete_replicaset_orphan( namespace, name):
    """
    Delete a ReplicaSet but orphan its Pods.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        delete_options = client.V1DeleteOptions(
            propagation_policy="Orphan"  # Equivalent to --cascade=orphan
        )
        response = apps_api.delete_namespaced_replica_set(
            name=name,
            namespace=namespace,
            body=delete_options
        )
        # return response
        return {"status": "success", "response": {
            "message": f"ReplicaSet {name} deleted with orphaned Pods.",
            "status": "success"
        }
}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message
