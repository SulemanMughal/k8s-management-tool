from django.http import JsonResponse


from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

import traceback
import json

# from django.http import JsonResponse

from .k8s_utils import create_stateful_set_with_storage

@csrf_exempt
def create_stateful_set_with_storage_view(request):

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

        # Create StatefulSet with dedicated storage

        response = create_stateful_set_with_storage(namespace, name, replicas, container_name, image, service_name, storage_size, ports, env_vars)

        if response["status"] == "error":

            return JsonResponse({"error": response["error"]}, status=400)

        return JsonResponse({"message": "StatefulSet created successfully with dedicated storage", "response": response["response"]})
