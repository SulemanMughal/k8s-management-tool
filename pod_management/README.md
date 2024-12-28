6. Key Features
Namespace Support:


Fetch logs for pods in specific namespaces.
Container Logs:


Optionally specify a container to fetch logs when a pod has multiple containers.
Tail Logs:


Limit the number of log lines retrieved using the tail_lines parameter.
Error Handling:


Provides descriptive error messages for issues like missing pods or invalid namespaces.





4. Example Usage
GET Request
Fetch logs for a specific pod:
GET /get-pod-logs/?namespace=default&pod_name=my-pod&tail_lines=50

Optionally specify the container name if the pod has multiple containers:
GET /get-pod-logs/?namespace=default&pod_name=my-pod&container_name=my-container&tail_lines=50


5. Example Response
Success
{
    "logs": "Log line 1\nLog line 2\nLog line 3\n..."
}

Error
{
    "error": "Pod not found in the specified namespace."
}



#------------------------


4. Example Usage
POST Request
Send a POST request to the port-forward/ endpoint with the following payload:
{
    "namespace": "default",
    "pod_name": "my-pod",
    "local_port": 8080,
    "pod_port": 80
}

Example Response
{
    "message": "Port forwarding established: localhost:8080 -> my-pod:80"
}


5. Notes
Port Forwarding Limitations:


Port forwarding requires the Kubernetes Python client to maintain an open WebSocket connection to the API server. Ensure the Django server is capable of maintaining long-running connections.
It works for as long as the connection remains active.
Local Port:


Ensure the local_port is available and not used by another process on the machine where the Django server is running.
Security:


Use authentication and authorization to restrict access to the port-forwarding feature.
Connection Termination:


The port-forwarding session will terminate if the WebSocket connection is closed.



#-----------------------


POST Request
Send a POST request to the endpoint create-pod-with-resources/ with the following JSON payload:
{
    "namespace": "default",
    "pod_name": "example-pod",
    "container_name": "example-container",
    "image": "nginx",
    "ports": "80,443",
    "resources": {
        "requests": {
            "cpu": "100m",
            "memory": "128Mi"
        },
        "limits": {
            "cpu": "500m",
            "memory": "512Mi"
        }
    }
}


Key Features
Resource Requests and Limits:


Requests: Guaranteed minimum resources for the container.
Limits: Maximum resources the container can consume.
Namespace Support:


Create Pods in specific namespaces.
Customizable Ports:


Specify container ports dynamically.




Example Response
Success
{
    "message": "Pod created successfully with resource requests and limits",
    "response": {
        "metadata": {
            "name": "example-pod",
            "namespace": "default",
            ...
        },
        "status": {
            ...
        }
    }
}

Error
{
    "error": "Invalid resources format"
}



Use Cases
Resource Management:


Ensure fair resource allocation among Pods in the cluster.
Prevent Resource Overuse:


Set maximum resource limits to prevent noisy neighbor issues.
Efficient Scheduling:


Help the Kubernetes scheduler optimize node utilization with resource requests.
