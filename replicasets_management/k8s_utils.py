from my_site.utils import load_custom_kubeconfig
from kubernetes import client
import traceback

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


def scale_stateful_set(namespace, name, replicas):

    """

    Scale an existing StatefulSet by modifying its replicas field.

    """

    # config.load_kube_config()

    # apps_v1 = client.AppsV1Api()
    core_api, apps_api, _,_ = load_custom_kubeconfig()

    try:

        # Get the existing StatefulSet

        stateful_set = apps_api.read_namespaced_stateful_set(name=name, namespace=namespace)

        # Modify the replicas field

        stateful_set.spec.replicas = replicas

        # Apply the updated StatefulSet configuration

        response = apps_api.replace_namespaced_stateful_set(name=name, namespace=namespace, body=stateful_set)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        traceback.print_exc()

        # return {"status": "error", "error": str(e)}
        return {"status": "error", "error": str(e.reason), "error-status": e.status}



def create_pvc_template(storage_size="1Gi"):
    """
    Create a PersistentVolumeClaim template for StatefulSet.
    """
    return client.V1PersistentVolumeClaim(
        metadata=client.V1ObjectMeta(name="data"),
        spec=client.V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteOnce"],
            resources=client.V1ResourceRequirements(
                requests={"storage": storage_size}
            ),
        ),
    )


def create_stateful_set(namespace, name, replicas, container_name, image, service_name, storage_size="1Gi", ports=None, env_vars=None):
    """
    Create a StatefulSet with associated PVCs.
    """
    # config.load_kube_config()
    # apps_v1 = client.AppsV1Api()
    core_api, apps_api, _,_ = load_custom_kubeconfig()

    # Define container specification
    container = client.V1Container(
        name=container_name,
        image=image,
        ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],
        env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],
        volume_mounts=[client.V1VolumeMount(name="data", mount_path="/data")],
    )

    # Define pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Define PVC template
    pvc_template = create_pvc_template(storage_size)

    # Define StatefulSet specification
    spec = client.V1StatefulSetSpec(
        service_name=service_name,
        replicas=replicas,
        selector=client.V1LabelSelector(match_labels={"app": name}),
        template=template,
        volume_claim_templates=[pvc_template],
    )

    # Define StatefulSet
    stateful_set = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )

    try:
        response = apps_api.create_namespaced_stateful_set(namespace=namespace, body=stateful_set)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        traceback.print_exc()
        return {"status": "error", "error": str(e)}
    

def create_replica_set_with_shared_pv(namespace, name, replicas, container_name, image, pvc_name, base_path, ports=None, env_vars=None):

    """

    Create a ReplicaSet where all pods share the same PersistentVolume but have separate subdirectories.

    """

    # config.load_kube_config()

    # apps_v1 = client.AppsV1Api()

    core_api, apps_api, _,_ = load_custom_kubeconfig()

    # Define container specifications

    containers = []

    for i in range(replicas):

        container = client.V1Container(

            name=f"{container_name}-{i}",

            image=image,

            volume_mounts=[

                client.V1VolumeMount(

                    name=pvc_name,

                    mount_path=f"{base_path}/pod-{i}",

                    sub_path=f"pod-{i}"  # Each pod will use its unique subdirectory

                )

            ],

            env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],

            ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],

        )

        containers.append(container)

    # Define volumes

    volumes = [client.V1Volume(

        name=pvc_name,

        persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=pvc_name),

    )]

    # Define pod template

    template = client.V1PodTemplateSpec(

        metadata=client.V1ObjectMeta(labels={"app": name}),

        spec=client.V1PodSpec(containers=containers, volumes=volumes),

    )

    # Define ReplicaSet specification

    spec = client.V1ReplicaSetSpec(

        replicas=replicas,

        selector=client.V1LabelSelector(match_labels={"app": name}),

        template=template,

    )

    # Define ReplicaSet

    replica_set = client.V1ReplicaSet(

        api_version="apps/v1",

        kind="ReplicaSet",

        metadata=client.V1ObjectMeta(name=name),

        spec=spec,

    )

    try:

        response = apps_api.create_namespaced_replica_set(namespace=namespace, body=replica_set)

        return {"status": "success", "response": response.to_dict()}

    except client.exceptions.ApiException as e:

        traceback.print_exc()

        return {"status": "error", "error": str(e)}


def create_persistent_volume_claim(namespace, pvc_name, storage_size="1Gi"):
    # config.load_kube_config()
    # v1 = client.CoreV1Api()

    core_api, apps_api, _,_ = load_custom_kubeconfig()

    pvc_body = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(name=pvc_name),
        spec=client.V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteOnce"],
            resources=client.V1ResourceRequirements(requests={"storage": storage_size}),
        ),
    )

    try:
        response = core_api.create_namespaced_persistent_volume_claim(namespace=namespace, body=pvc_body)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        traceback.print_exc()
        return {"status": "error", "error": str(e)}



def create_replica_set_with_separate_pvcs(namespace, name, replicas, container_name, image, mount_path, storage_size="1Gi", ports=None, env_vars=None):
    # config.load_kube_config()
    # apps_v1 = client.AppsV1Api()

    core_api, apps_api, _,_ = load_custom_kubeconfig()

    # Create PVCs for each replica
    pvc_names = [f"{name}-pvc-{i}" for i in range(replicas)]
    for pvc_name in pvc_names:
        pvc_response = create_persistent_volume_claim(namespace, pvc_name, storage_size)
        if pvc_response["status"] == "error":
            return pvc_response

    # Define container specification
    containers = []
    volumes = []
    for i, pvc_name in enumerate(pvc_names):
        container = client.V1Container(
            name=f"{container_name}-{i}",
            image=image,
            volume_mounts=[client.V1VolumeMount(name=pvc_name, mount_path=mount_path)],
            env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],
            ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],
        )
        containers.append(container)
        volumes.append(client.V1Volume(
            name=pvc_name,
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=pvc_name),
        ))

    # Define pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=containers, volumes=volumes),
    )

    # Define ReplicaSet specification
    spec = client.V1ReplicaSetSpec(
        replicas=replicas,
        selector=client.V1LabelSelector(match_labels={"app": name}),
        template=template,
    )

    # Define ReplicaSet
    replica_set = client.V1ReplicaSet(
        api_version="apps/v1",
        kind="ReplicaSet",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )

    try:
        response = apps_api.create_namespaced_replica_set(namespace=namespace, body=replica_set)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:

        traceback.print_exc()
        return {"status": "error", "error": str(e)}
