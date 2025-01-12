from django.http import JsonResponse
from .k8s_utils import  create_replicaset, list_replicasets, scale_replicaset, update_replicaset, get_replicaset_status, delete_replicaset, get_replicaset_pods, get_replicaset_events, get_replicaset_logs, delete_replicaset_orphan, scale_stateful_set, create_stateful_set, create_replica_set_with_shared_pv, create_replica_set_with_separate_pvcs
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_replica_set_with_separate_pvcs_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        namespace = data.get("namespace", "default")
        name = data.get("name")
        replicas = int(data.get("replicas", 1))
        container_name = data.get("container_name")
        image = data.get("image")
        mount_path = data.get("mount_path")
        storage_size = data.get("storage_size", "1Gi")
        ports = data.get("ports", "")
        env_vars = data.get("env_vars", {})

        # Parse ports and environment variables
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            # env_vars = eval(env_vars) if env_vars else {}
        except:
            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        # Create ReplicaSet with Separate PVCs
        response = create_replica_set_with_separate_pvcs(namespace, name, replicas, container_name, image, mount_path, storage_size, ports, env_vars)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "ReplicaSet created successfully with separate PVCs", "response": response["response"]})


@csrf_exempt
def create_replica_set_with_shared_pv_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        namespace = data.get("namespace", "default")

        name = data.get("name")

        replicas = int(data.get("replicas", 1))

        container_name = data.get("container_name")

        image = data.get("image")

        pvc_name = data.get("pvc_name")

        base_path = data.get("base_path", "/data")

        ports = data.get("ports", "")

        env_vars = data.get("env_vars", {})

        # Parse ports and environment variables

        try:

            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]

            # env_vars = eval(env_vars) if env_vars else {}

        except:

            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        # Create ReplicaSet with Shared PersistentVolume

        response = create_replica_set_with_shared_pv(namespace, name, replicas, container_name, image, pvc_name, base_path, ports, env_vars)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "ReplicaSet created successfully with shared PersistentVolume", "response": response["response"]})


@csrf_exempt
def create_stateful_set_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        namespace = data.get("namespace", "default")
        name = data.get("name")
        replicas = int(data.get("replicas", 1))
        container_name = data.get("container_name")
        image = data.get("image")
        service_name = data.get("service_name")
        storage_size = data.get("storage_size", "1Gi")
        ports = data.get("ports", "")
        env_vars = data.get("env_vars", {})

        # Parse ports and environment variables
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            # env_vars = eval(env_vars) if env_vars else {}
        except:
            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        # Create StatefulSet
        response = create_stateful_set(namespace, name, replicas, container_name, image, service_name, storage_size, ports, env_vars)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "StatefulSet created successfully", "response": response["response"]})


@csrf_exempt
def scale_stateful_set_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        namespace = data.get("namespace", "default")

        name = data.get("name")

        replicas = int(data.get("replicas", 1))

        if not name:

            return JsonResponse({"error": "StatefulSet name is required"}, status=400)

        # Scale the StatefulSet

        response = scale_stateful_set(namespace, name, replicas)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "StatefulSet scaled successfully", "response": response["response"]})



def list_replicasets_view(request, namespace):
    try:
        response = list_replicasets( namespace)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def create_replicaset_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        replicaName = data.get("name")
        namespace = data.get("namespace")
        labels = data.get("labels")
        replicas = int(data.get("replicas", 1))
        match_labels = data.get("match_labels")
        container_name = data.get("containerName")
        container_image = data.get("containerImage")
        container_port = int(data.get("containerPort", 80))
        response = create_replicaset( namespace, replicaName, labels, replicas, match_labels, container_name, container_image, container_port)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def update_replicate_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        replicaName = data.get("name")
        namespace = data.get("namespace")
        replicas = int(data.get("replicas", 1))
        response = update_replicaset( namespace, replicaName, replicas)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_replicate_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = get_replicaset_status( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_replicate_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = delete_replicaset( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_replicate_pods_view(request):
    try:
        namespace = request.GET.get("namespace")
        labels = request.GET.get("labels")
        response = get_replicaset_pods( namespace, labels)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_replicate_events_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = get_replicaset_events( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_replicate_logs_view(request):
    try:
        namespace = request.GET.get("namespace")
        pod_name = request.GET.get("pod_name")
        container_name = request.GET.get("container_name")
        response = get_replicaset_logs( namespace, pod_name, container_name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def delete_replicate_orphan_view(request):
    try:
        namespace = request.GET.get("namespace")
        name = request.GET.get("name")
        response = delete_replicaset_orphan( namespace, name)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=response["error-status"])
        return JsonResponse({"response": response["response"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)