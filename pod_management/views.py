
from django.http import JsonResponse

from .k8s_utils import create_pod, get_pod, update_pod, delete_pod, list_pods,port_forward_pod, get_pod_logs, create_pod_with_resources, create_pod_with_startup_probe, create_pod_with_liveness_probe, create_pod_with_readiness_probe


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



def update_pod_view(request):

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

        response = update_pod(namespace, pod_name, container_name, image, ports, env_vars)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "Pod updated successfully", "response": response["response"]})



def delete_pod_view(request):

    if request.method == "POST":

        namespace = request.POST.get("namespace", "default")

        pod_name = request.POST.get("pod_name")

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



def create_pod_with_resources_view(request):
    if request.method == "POST":
        namespace = request.POST.get("namespace", "default")
        pod_name = request.POST.get("pod_name")
        container_name = request.POST.get("container_name")
        image = request.POST.get("image")
        ports = request.POST.get("ports", "")
        resources = request.POST.get("resources")

        if not pod_name or not container_name or not image or not resources:
            return JsonResponse({"error": "Pod name, container name, image, and resources are required"}, status=400)

        # Parse ports and resources
        try:
            ports = [int(port.strip()) for port in ports.split(",") if port.strip()]
            resources = eval(resources)  # Example: '{"requests": {"cpu": "100m", "memory": "128Mi"}, "limits": {"cpu": "500m", "memory": "512Mi"}}'
        except:
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
