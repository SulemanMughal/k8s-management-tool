from my_site.utils import load_custom_kubeconfig
from kubernetes import client
import traceback

def create_pvc_template(storage_size="1Gi"):
    """
    Create a PersistentVolumeClaim template for StatefulSet.
    Each pod in the StatefulSet will receive a unique PVC based on this template.
    """
    return client.V1PersistentVolumeClaim(

        metadata=client.V1ObjectMeta(name="data"),  # PVC name prefix

        spec=client.V1PersistentVolumeClaimSpec(

            access_modes=["ReadWriteOnce"],

            resources=client.V1ResourceRequirements(

                requests={"storage": storage_size}

            ),

        ),

    )


def create_stateful_set_with_storage(namespace, name, replicas, container_name, image, service_name, storage_size="1Gi", ports=None, env_vars=None):

    """

    Create a StatefulSet where each pod has stable, dedicated storage.

    """

    # config.load_kube_config()

    # apps_v1 = client.AppsV1Api()
    core_api, apps_api, networking_api, custom_api = load_custom_kubeconfig()

    # Define container specification

    container = client.V1Container(

        name=container_name,

        image=image,

        ports=[client.V1ContainerPort(container_port=p) for p in (ports or [])],

        env=[client.V1EnvVar(name=k, value=v) for k, v in (env_vars or {}).items()],

        volume_mounts=[

            client.V1VolumeMount(name="data", mount_path="/data")  # Mount unique storage

        ],

    )

    # Define pod template

    template = client.V1PodTemplateSpec(

        metadata=client.V1ObjectMeta(labels={"app": name}),

        spec=client.V1PodSpec(containers=[container]),

    )

    # Define PVC template for storage

    pvc_template = create_pvc_template(storage_size)

    # Define StatefulSet specification

    spec = client.V1StatefulSetSpec(

        service_name=service_name,

        replicas=replicas,

        selector=client.V1LabelSelector(match_labels={"app": name}),

        template=template,

        volume_claim_templates=[pvc_template],  # Assign unique PVCs to pods

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

        # return {"status": "error", "error": str(e)}
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
