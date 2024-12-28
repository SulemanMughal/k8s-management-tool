
from django.http import JsonResponse

from .k8s_utils import create_pod, get_pod, update_pod, delete_pod, list_pods,port_forward_pod, get_pod_logs


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
