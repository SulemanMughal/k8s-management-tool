
from django.http import JsonResponse

from .k8s_utils import create_pod, get_pod, update_pod, delete_pod, list_pods,port_forward_pod, get_pod_logs, create_pod_with_resources, create_pod_with_startup_probe, create_pod_with_liveness_probe, create_pod_with_readiness_probe, create_pod_with_security_context, set_namespace_psa_labels, create_pod_psa_compliant, get_kube_proxy_pods, get_pods_by_label_selector, list_container_images, create_persistent_volume_claim, create_replica_set, create_service
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json

import traceback


@csrf_exempt
def create_pod_with_service_and_pvc_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        namespace = data.get("namespace", "default")

        name = data.get("name")

        container_name = data.get("container_name")

        image = data.get("image")

        pvc_name = data.get("pvc_name")

        mount_path = data.get("mount_path", "/data")

        service_name = data.get("service_name")

        ports = data.get("ports", "80")

        target_port = int(data.get("target_port", 80))

        storage_size = data.get("storage_size", "1Gi")

        env_vars = data.get("env_vars", {})

        # Parse ports and environment variables

        try:

            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]

            # env_vars = eval(env_vars) if env_vars else {}

        except:

            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        # Create PVC

        pvc_response = create_persistent_volume_claim(namespace, pvc_name, storage_size)

        if pvc_response["status"] == "error":

            return JsonResponse({"error": f"PVC creation failed: {pvc_response['error']}"}, status=400)

        # Create ReplicaSet

        rs_response = create_replica_set(namespace, name, container_name, image, pvc_name, mount_path, ports, env_vars)

        if rs_response["status"] == "error":

            return JsonResponse({"error": f"ReplicaSet creation failed: {rs_response['error']}"}, status=400)

        # Create Service

        svc_response = create_service(namespace, service_name, name, ports[0], target_port)

        if svc_response["status"] == "error":

            return JsonResponse({"error": f"Service creation failed: {svc_response['error']}"}, status=400)

        return JsonResponse({

            "message": "Pod with dedicated PVC and Service created successfully",

            "pvc_response": pvc_response["response"],

            "replica_set_response": rs_response["response"],

            "service_response": svc_response["response"]

        })


def create_pod_view(request):

    if request.method == "POST":

        namespace = request.POST.get("namespace", "default")

        pod_name = request.POST.get("pod_name")

        container_name = request.POST.get("container_name")

        image = request.POST.get("image")

        ports = request.POST.get("ports", "")

        env_vars = request.POST.get("env_vars", "{}")

        try:

            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]

            env_vars = eval(env_vars) if env_vars else {}

        except:

            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        response = create_pod(namespace, pod_name, container_name, image, ports, env_vars)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "Pod created successfully", "response": response["response"]})



def get_pod_view(request):

    if request.method == "GET":

        namespace = request.GET.get("namespace", "default")

        pod_name = request.GET.get("pod_name")

        if not pod_name:

            return JsonResponse({"error": "Pod name is required"}, status=400)

        response = get_pod(namespace, pod_name)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"response": response["response"]})



@csrf_exempt
def update_pod_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        namespace = data.get("namespace", "default")
        pod_name = data.get("pod_name")
        container_name = data.get("container_name")
        image = data.get("image")
        ports = data.get("ports", "")
        env_vars = data.get("env_vars", {})

        try:

            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]

            # env_vars = eval(env_vars) if env_vars else {}

        except:

            return JsonResponse({"error": "Invalid ports or environment variables format"}, status=400)

        response = update_pod(namespace, pod_name, container_name, image, ports, env_vars)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "Pod updated successfully", "response": response["response"]})


@csrf_exempt
def delete_pod_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        namespace = data.get("namespace", "default")

        pod_name = data.get("pod_name")

        if not pod_name:

            return JsonResponse({"error": "Pod name is required"}, status=400)

        response = delete_pod(namespace, pod_name)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "Pod deleted successfully", "response": response["response"]})



def list_pods_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace", None)  # Optional namespace filter
        response = list_pods(namespace)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"pods": response["pods"]})




def port_forward_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        local_port = int(request.POST.get("local_port"))
        pod_port = int(request.POST.get("pod_port"))

        if not pod_name or not local_port or not pod_port:
            return JsonResponse({"error": "Pod name, local port, and pod port are required"}, status=400)

        response = port_forward_pod(namespace, pod_name, local_port, pod_port)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": response["message"]})



def get_pod_logs_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace", "default")
        pod_name = request.GET.get("pod_name")
        container_name = request.GET.get("container_name", None)  # Optional
        tail_lines = int(request.GET.get("tail_lines", 100))  # Default to 100 lines

        if not pod_name:
            return JsonResponse({"error": "Pod name is required"}, status=400)

        response = get_pod_logs(namespace, pod_name, container_name, tail_lines)

        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"logs": response["logs"]})


@csrf_exempt
def create_pod_with_resources_view(request):
    if request.method == "POST":
        # print(request.body)
        data = json.loads(request.body)

        namespace = data.get("namespace", "default")
        pod_name = data.get("pod_name")
        container_name = data.get("container_name")
        image = data.get("image")
        ports = data.get("ports", "")
        resources = data.get("resources")

        print(data)

        if not pod_name or not container_name or not image or not resources:
            return JsonResponse({"error": "Pod name, container name, image, and resources are required"}, status=400)

        # Parse ports and resources
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            # resources = eval(resources)  # Example: '{"requests": {"cpu": "100m", "memory": "128Mi"}, "limits": {"cpu": "500m", "memory": "512Mi"}}'
        except :
            traceback.print_exc()
            return JsonResponse({"error": "Invalid ports or resources format"}, status=400)

        response = create_pod_with_resources(namespace, pod_name, container_name, image, resources, ports)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "Pod created successfully with resource requests and limits", "response": response["response"]})




def create_pod_with_startup_probe_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        probe_command = request.POST.getlist("probe_command")  # Example: ["cat", "/tmp/healthy"]
        initial_delay_seconds = int(request.POST.get("initial_delay_seconds", 10))
        period_seconds = int(request.POST.get("period_seconds", 5))
        failure_threshold = int(request.POST.get("failure_threshold", 30))
        ports = request.POST.get("ports", "")

        if not pod_name or not container_name or not image or not probe_command:
            return JsonResponse({"error": "Pod name, container name, image, and probe command are required"}, status=400)

        # Parse ports
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
        except:
            return JsonResponse({"error": "Invalid ports format"}, status=400)

        response = create_pod_with_startup_probe(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            image=image,
            probe_command=probe_command,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            failure_threshold=failure_threshold,
            ports=ports,
        )
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "Pod created successfully with startupProbe", "response": response["response"]})




def create_pod_with_liveness_probe_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        probe_command = request.POST.getlist("probe_command")  # Example: ["cat", "/tmp/healthy"]
        initial_delay_seconds = int(request.POST.get("initial_delay_seconds", 10))
        period_seconds = int(request.POST.get("period_seconds", 5))
        failure_threshold = int(request.POST.get("failure_threshold", 3))
        success_threshold = int(request.POST.get("success_threshold", 1))
        ports = request.POST.get("ports", "")

        if not pod_name or not container_name or not image or not probe_command:
            return JsonResponse({"error": "Pod name, container name, image, and probe command are required"}, status=400)

        # Parse ports
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
        except:
            return JsonResponse({"error": "Invalid ports format"}, status=400)

        response = create_pod_with_liveness_probe(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            image=image,
            probe_command=probe_command,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            ports=ports,
        )
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "Pod created successfully with livenessProbe", "response": response["response"]})




def create_pod_with_readiness_probe_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        probe_command = request.POST.getlist("probe_command")  # Example: ["cat", "/tmp/ready"]
        http_get_path = request.POST.get("http_get_path", None)
        http_get_port = request.POST.get("http_get_port", None)
        tcp_socket_port = request.POST.get("tcp_socket_port", None)
        initial_delay_seconds = int(request.POST.get("initial_delay_seconds", 5))
        period_seconds = int(request.POST.get("period_seconds", 10))
        failure_threshold = int(request.POST.get("failure_threshold", 3))
        success_threshold = int(request.POST.get("success_threshold", 1))
        ports = request.POST.get("ports", "")

        if not pod_name or not container_name or not image:
            return JsonResponse({"error": "Pod name, container name, and image are required"}, status=400)

        # Parse ports
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            if http_get_port:
                http_get_port = int(http_get_port)
            if tcp_socket_port:
                tcp_socket_port = int(tcp_socket_port)
        except:
            return JsonResponse({"error": "Invalid ports format"}, status=400)

        try:
            response = create_pod_with_readiness_probe(
                namespace=namespace,
                pod_name=pod_name,
                container_name=container_name,
                image=image,
                probe_command=probe_command,
                http_get_path=http_get_path,
                http_get_port=http_get_port,
                tcp_socket_port=tcp_socket_port,
                initial_delay_seconds=initial_delay_seconds,
                period_seconds=period_seconds,
                failure_threshold=failure_threshold,
                success_threshold=success_threshold,
                ports=ports,
            )
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=400)
            return JsonResponse({"message": "Pod created successfully with readinessProbe", "response": response["response"]})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)



def create_pod_with_security_context_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        security_context = request.POST.get("security_context", None)
        ports = request.POST.get("ports", "")

        if not pod_name or not container_name or not image:
            return JsonResponse({"error": "Pod name, container name, and image are required"}, status=400)

        # Parse ports and security_context
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            security_context = eval(security_context) if security_context else None
        except:
            return JsonResponse({"error": "Invalid ports or security_context format"}, status=400)

        response = create_pod_with_security_context(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            image=image,
            security_context=security_context,
            ports=ports,
        )
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": "Pod created successfully with SecurityContext", "response": response["response"]})



def set_namespace_psa_labels_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        psa_level = request.POST.get("psa_level", "baseline")  # Default to baseline

        if not namespace or not psa_level:
            return JsonResponse({"error": "Namespace and PSA level are required"}, status=400)

        response = set_namespace_psa_labels(namespace, psa_level)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": f"PSA labels applied to namespace {namespace}", "response": response["response"]})




def create_pod_psa_compliant_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        security_context = request.POST.get("security_context", "{}")
        psa_level = request.POST.get("psa_level", "baseline")
        ports = request.POST.get("ports", "")

        if not pod_name or not container_name or not image or not psa_level:
            return JsonResponse({"error": "Pod name, container name, image, and PSA level are required"}, status=400)

        # Parse ports and security_context
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            security_context = eval(security_context)
        except:
            return JsonResponse({"error": "Invalid ports or security_context format"}, status=400)

        response = create_pod_psa_compliant(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            image=image,
            security_context=security_context,
            psa_level=psa_level,
            ports=ports,
        )
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"message": f"Pod {pod_name} created in namespace {namespace}", "response": response["response"]})




def get_kube_proxy_pods_view(request):
    if request.method == "GET":
        namespace = request.GET.get("namespace", "kube-system")  # Default to kube-system

        response = get_kube_proxy_pods(namespace)
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"pods": response["pods"]})



def get_pods_by_label_selector_view(request):
    if request.method == "GET":
        # )
        namespace = request.GET.get("namespace", "default")
        label_selector = request.GET.get("label_selector", "")

        try:
            response = get_pods_by_label_selector(namespace, label_selector)
            if response["status"] == "error":
                return JsonResponse({"error": response["error"]}, status=400)
            return JsonResponse({"pods": response["pods"]})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(['GET'])
def list_container_images_views(request):
    try:
        response = list_container_images()
        if response["status"] == "error":
            return JsonResponse({"error": response["error"]}, status=400)
        return JsonResponse({"images": response["images"]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)