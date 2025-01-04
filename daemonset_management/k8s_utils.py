from my_site.utils import load_custom_kubeconfig
from kubernetes import client
import json
import time
from datetime import datetime


def create_daemonset_object(objName, objLabels, matchLabels, templateLabels, containerName, containerImage):
    """
    Create a DaemonSet object equivalent to the provided YAML.
    """
    return client.V1DaemonSet(
        metadata=client.V1ObjectMeta(
            name=objName,
            labels=objLabels
        ),
        spec=client.V1DaemonSetSpec(
            selector=client.V1LabelSelector(
                match_labels=matchLabels
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=templateLabels),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=containerName,
                            image=containerImage
                        )
                    ]
                )
            )
        )
    )




def create_daemonset( namespace, objName, objLabels, matchLabels, templateLabels, containerName, containerImage):
    """
    Create the DaemonSet in the specified namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    daemonset = create_daemonset_object(objName, objLabels, matchLabels, templateLabels, containerName, containerImage)
    try:
        response = apps_api.create_namespaced_daemon_set(
            namespace=namespace,
            body=daemonset
        )
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error creating DaemonSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message




def describe_daemonset( namespace, name):
    """
    Describe a DaemonSet and its details.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonset = apps_api.read_namespaced_daemon_set(name=name, namespace=namespace)
        details = {
            "name": daemonset.metadata.name,
            "labels": daemonset.metadata.labels,
            "containers": [{"name": c.name, "image": c.image} for c in daemonset.spec.template.spec.containers],
            "desired_number_scheduled": daemonset.status.desired_number_scheduled,
            "current_number_scheduled": daemonset.status.current_number_scheduled,
        }
        return {"status": "success", "response": details}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error describing DaemonSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message




def update_daemonset_image( namespace, objName, containerName,  newContainerImage):
    """
    Update the image of the DaemonSet's container.
    """
    try:
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {"name": containerName, "image": newContainerImage}
                        ]
                    }
                }
            }
        }
        core_api, apps_api = load_custom_kubeconfig()
        response = apps_api.patch_namespaced_daemon_set(
            name=objName,
            namespace=namespace,
            body=patch_body
        )
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error updating DaemonSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message
    

def delete_daemonset( namespace, name):
    """
    Delete a DaemonSet.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.delete_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions()
        )
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error deleting DaemonSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status" : e.status} # Return error message



def list_daemonsets(namespace):
    """
    List DaemonSets in a given namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        response = apps_api.list_namespaced_daemon_set(namespace=namespace)
        daemonsets = [ds.metadata.name for ds in response.items]
        return {"status": "success", "response": daemonsets}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message
    



def get_pods_managed_by_daemonsets(namespace):
    """
    Get pods managed by DaemonSets in a given namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonsets = apps_api.list_namespaced_daemon_set(namespace=namespace).items
        pods = []
        for ds in daemonsets:
            selector = ds.spec.selector.match_labels
            label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])
            ds_pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector).items
            for pod in ds_pods:
                pods.append(pod.metadata.name)
        return {"status": "success", "response": pods}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def get_pods_managed_by_specific_daemonset(namespace, daemonset_name):
    """
    Get pods managed by a specific DaemonSet in a given namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonset = apps_api.read_namespaced_daemon_set(name=daemonset_name, namespace=namespace)
        selector = daemonset.spec.selector.match_labels
        label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])
        pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector).items
        pod_names = [pod.metadata.name for pod in pods]
        return {"status": "success", "response": pod_names}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def update_daemonset_node_selector( namespace, name, node_selector):
    """
    Update the DaemonSet with a nodeSelector to restrict it to specific nodes.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "nodeSelector": node_selector
                    }
                }
            }
        }
        response = apps_api.patch_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error updating DaemonSet with nodeSelector: {e}")
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message



def update_daemonset_node_affinity( namespace, name, match_labels):
    """
    Update the DaemonSet with nodeAffinity to restrict it to specific nodes.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "affinity": {
                            "nodeAffinity": {
                                "requiredDuringSchedulingIgnoredDuringExecution": {
                                    "nodeSelectorTerms": [
                                        {
                                            "matchExpressions": [
                                                {
                                                    "key": key,
                                                    "operator": "In",
                                                    "values": [value],
                                                }
                                                for key, value in match_labels.items()
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
        response = apps_api.patch_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error updating DaemonSet with nodeAffinity: {e}")
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message



def pause_daemonset( namespace, name):
    """
    Mimic pausing a DaemonSet by removing nodeSelector or setting a taint.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "nodeSelector": None  # Remove nodeSelector to prevent scheduling
                    }
                }
            }
        }
        response = apps_api.patch_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        # return response
        # return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error pausing DaemonSet: {e}")
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message


def resume_daemonset( namespace, name, node_selector):
    """
    Resume a DaemonSet by re-adding the nodeSelector.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "nodeSelector": node_selector
                    }
                }
            }
        }
        response = apps_api.patch_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message


def get_nodes_for_daemonset(namespace, daemonset_name):
    """
    Get the nodes on which a specific DaemonSet is deployed.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonset = apps_api.read_namespaced_daemon_set(name=daemonset_name, namespace=namespace)
        selector = daemonset.spec.selector.match_labels
        label_selector = ",".join([f"{key}={value}" for key, value in selector.items()])
        pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector).items
        nodes = [pod.spec.node_name for pod in pods]
        return {"status": "success", "response": nodes}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def change_daemonset_namespace(current_namespace, daemonset_name, new_namespace):
    """
    Change the namespace of a DaemonSet by recreating it in the new namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        # Get the existing DaemonSet
        daemonset = apps_api.read_namespaced_daemon_set(name=daemonset_name, namespace=current_namespace)
        
        # Create a new DaemonSet in the new namespace
        daemonset.metadata.namespace = new_namespace
        daemonset.metadata.resource_version = None  # Clear resource version to create a new object
        response = apps_api.create_namespaced_daemon_set(namespace=new_namespace, body=daemonset)
        
        # Delete the old DaemonSet
        apps_api.delete_namespaced_daemon_set(name=daemonset_name, namespace=current_namespace, body=client.V1DeleteOptions())
        
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # print(json.loads(e.body)["message"])
        # print(dir(e))
        return {"status": "error", "error": str(json.loads(e.body)["message"]), "error-status": e.status}
    

def daemonset_rollout_status( namespace, name):
    """
    Get the rollout status of a DaemonSet.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonset = apps_api.read_namespaced_daemon_set_status(name=name, namespace=namespace)
        desired_number_scheduled = daemonset.status.desired_number_scheduled
        current_number_scheduled = daemonset.status.current_number_scheduled
        number_ready = daemonset.status.number_ready

        if desired_number_scheduled == current_number_scheduled == number_ready:
            details =  {
                "status": "Successful",
                "message": f"DaemonSet {name} has rolled out successfully. All {desired_number_scheduled} Pods are ready."
            }
            return {"status": "success", "response": details}
        else:
            details =  {
                "status": "In Progress",
                "message": f"DaemonSet {name} is rolling out. Desired: {desired_number_scheduled}, Current: {current_number_scheduled}, Ready: {number_ready}."
            }
            return {"status": "success", "response": details}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error getting rollout status for DaemonSet {name}: {e}")
        return {"status": "error", "error": str(json.loads(e.body)["message"]), "error-status": e.status}



def daemonset_rollout_status_periodic(namespace, name, timeout=300, interval=10):
    """
    Get the rollout status of a DaemonSet with periodic polling until the rollout completes.
    """
    core_api, apps_api = load_custom_kubeconfig()
    start_time = time.time()
    
    while True:
        try:
            daemonset = apps_api.read_namespaced_daemon_set_status(name=name, namespace=namespace)
            desired_number_scheduled = daemonset.status.desired_number_scheduled
            current_number_scheduled = daemonset.status.current_number_scheduled
            number_ready = daemonset.status.number_ready

            if desired_number_scheduled == current_number_scheduled == number_ready:
                details = {
                    "status": "Successful",
                    "message": f"DaemonSet {name} has rolled out successfully. All {desired_number_scheduled} Pods are ready."
                }
                return {"status": "success", "response": details}
            else:
                details = {
                    "status": "In Progress",
                    "message": f"DaemonSet {name} is rolling out. Desired: {desired_number_scheduled}, Current: {current_number_scheduled}, Ready: {number_ready}."
                }
                # print(details["message"])

            # Check if timeout has been reached
            if time.time() - start_time > timeout:
                details = {
                    "status": "Timeout",
                    "message": f"DaemonSet {name} rollout timed out. Desired: {desired_number_scheduled}, Current: {current_number_scheduled}, Ready: {number_ready}."
                }
                return {"status": "error", "response": details}

            # Wait for the specified interval before checking again
            time.sleep(interval)
        
        except client.exceptions.ApiException as e:
            return {"status": "error", "error": str(json.loads(e.body)["message"]), "error-status": e.status}
        

def get_daemonset_events(namespace, daemonset_name):
    """
    Get events for a specific DaemonSet in a given namespace.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        # List all events in the namespace
        events = core_api.list_namespaced_event(namespace=namespace).items
        # Filter events related to the DaemonSet
        daemonset_events = [event for event in events if event.involved_object.kind == "DaemonSet" and event.involved_object.name == daemonset_name]
        # Convert events to a list of dictionaries
        events_list = [{"message": event.message, "reason": event.reason, "type": event.type, "timestamp": event.last_timestamp} for event in daemonset_events]
        return {"status": "success", "response": events_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status} # Return error message
    

def update_rollout_history( namespace, name, new_image):
    """
    Update the rollout history in the DaemonSet annotations.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        # Retrieve the existing DaemonSet
        daemonset = apps_api.read_namespaced_daemon_set(name=name, namespace=namespace)
        annotations = daemonset.metadata.annotations or {}
        history = json.loads(annotations.get("rollout-history", "[]"))

        # Add the new rollout entry
        history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "image": new_image
        })

        # Update the annotations
        annotations["rollout-history"] = json.dumps(history)
        patch_body = {"metadata": {"annotations": annotations}}

        response = apps_api.patch_namespaced_daemon_set(
            name=name,
            namespace=namespace,
            body=patch_body
        )
        # return response
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error updating rollout history: {e}")
        return {"status": "error", "error": str(json.loads(e.body)["message"]), "error-status": e.status} # Return error message


def get_rollout_history(namespace, name):
    """
    Get the rollout history from the DaemonSet annotations.
    """
    core_api, apps_api = load_custom_kubeconfig()
    try:
        daemonset = apps_api.read_namespaced_daemon_set(name=name, namespace=namespace)
        annotations = daemonset.metadata.annotations or {}
        history = json.loads(annotations.get("rollout-history", "[]"))
        # return history
        return {"status": "success", "response": history}
    except client.exceptions.ApiException as e:
        # raise Exception(f"Error fetching rollout history: {e}")
        return {"status": "error", "error": str(json.loads(e.body)["message"]), "error-status": e.status} # Return error message
