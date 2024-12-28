from my_site.utils import load_custom_kubeconfig
from kubernetes import client


# Designing ReplicaSets
def create_replicaset_object(name, namespace, image, replicas, labels):
    return client.V1ReplicaSet(
        metadata=client.V1ObjectMeta(name=name, labels=labels),
        spec=client.V1ReplicaSetSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name=name,
                        image=image,
                        ports=[client.V1ContainerPort(container_port=80)]
                    )
                ])
            )
        )
    )


# Creating ReplicaSets
def create_replicaset( namespace, replicaset):
    core_api, apps_api = load_custom_kubeconfig()
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
