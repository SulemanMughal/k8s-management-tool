from my_site.utils import load_custom_kubeconfig
from kubernetes import client



def create_deployment_object(name, namespace, image, replicas, labels):
    return client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name=name,
                        image=image,
                        ports=[client.V1ContainerPort(container_port=80)],
                    )
                ]),
            ),
        ),
    )



# Creating Deployments
def create_deployment( namespace, deployment):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.create_namespaced_deployment(
            namespace=namespace, body=deployment
        )
        # print(f"Deployment {deployment.metadata.name} created.")
        # return api_response
        # print(response)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # print(f"Exception when creating deployment: {e}")
        print(e)
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message




# Updating Deployments
def update_deployment( namespace, name, container_name, new_image):
    core_api, apps_api = load_custom_kubeconfig()
    """
    Update the image of a container in a Kubernetes Deployment.

    :param api_instance: AppsV1Api instance
    :param namespace: Namespace of the Deployment
    :param name: Name of the Deployment
    :param container_name: Name of the container to update
    :param new_image: New image to apply to the container
    :return: Success or error message with details
    """
    try:
        # Define the patch body to update the container image
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": container_name,
                                "image": new_image,
                            }
                        ]
                    }
                }
            }
        }

        # Apply the patch to the Deployment
        response = apps_api.patch_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        print(e)
        return {"status": "error", "error": str(e.reason), "error-status": e.status}


# Monitoring Deployment Status
def get_deployment_status( namespace, name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.read_namespaced_deployment(
            name=name, namespace=namespace
        )
        status = {
            "available_replicas": response.status.available_replicas,
            "ready_replicas": response.status.ready_replicas,
            "updated_replicas": response.status.updated_replicas,
            "replicas": response.status.replicas,
        }
        # print(f"Deployment {name} status: {status}")
        # return status
        return {"status": "success", "response": status}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message


# Deployment Strategies
def create_deployment_with_strategy(name, namespace, image, replicas, labels, strategy):
    # core_api, apps_api = load_custom_kubeconfig()
    return client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name=name,
                        image=image,
                        ports=[client.V1ContainerPort(container_port=80)],
                    )
                ]),
            ),
            strategy=client.V1DeploymentStrategy(type=strategy),
        ),
    )


# Deleting Deployments
def delete_deployment( namespace, name):
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.delete_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions(),
        )
        # print(f"Deployment {name} deleted.")
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # print(f"Exception when deleting deployment: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message
