from my_site.utils import load_custom_kubeconfig
from kubernetes import client
# import json
import ipaddress

def list_all_network_policies():
    """
    List all network policies available in Kubernetes across all namespaces.
    """
    core_api, apps_api, networking_api = load_custom_kubeconfig()
    try:
        network_policies = networking_api.list_network_policy_for_all_namespaces().items
        network_policy_list = [
            {
                "namespace": policy.metadata.namespace,
                "name": policy.metadata.name,
                "pod_selector": policy.spec.pod_selector.match_labels,
                "policy_types": policy.spec.policy_types
            }
            for policy in network_policies
        ]
        return {"status": "success", "response": network_policy_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def create_network_policy(namespace, policy_name, pod_selector, policy_types, match_labels):
    """
    Create a new network policy in Kubernetes.
    """
    _, _ , networking_api = load_custom_kubeconfig()
    ingress_rules = [
    client.V1NetworkPolicyIngressRule(
        _from=[
            client.V1NetworkPolicyPeer(
                pod_selector=client.V1LabelSelector(
                    match_labels={"app": "example"}
                )
            )
        ]
    )
]
    egress_rules = [
    client.V1NetworkPolicyEgressRule(
        to=[
            client.V1NetworkPolicyPeer(
                pod_selector=client.V1LabelSelector(
                    match_labels={"app": "example"}
                )
            )
        ]
    )
    ]
    # print(ingress_rules, egress_rules)
    # network_policy = client.V1NetworkPolicy(
    #     metadata=client.V1ObjectMeta(name=policy_name),
    #     spec=client.V1NetworkPolicySpec(
    #         pod_selector=client.V1LabelSelector(match_labels=pod_selector),
    #         policy_types=policy_types,
    #         ingress=ingress_rules,
    #         egress=egress_rules
    #     )
    # )
    network_policy = client.V1NetworkPolicy(
        metadata=client.V1ObjectMeta(name=policy_name),
        spec=client.V1NetworkPolicySpec(
            pod_selector=client.V1LabelSelector(match_labels=pod_selector),
            policy_types=policy_types,
            ingress=ingress_rules,
            egress=egress_rules
        )
    )
    try:
        response = networking_api.create_namespaced_network_policy(namespace=namespace, body=network_policy)
        return {"status": "success", "response": response.to_dict()}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    


def list_all_ip_pools():
    """
    List all IP Pools available in Kubernetes (using Calico).
    """
    _, _ , _, custom_api = load_custom_kubeconfig()
    try:
        ip_pools = custom_api.list_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools"
        )
        ip_pool_list = [
            {
                "name": pool["metadata"]["name"],
                "cidr": pool["spec"]["cidr"],
                "ipipMode": pool["spec"].get("ipipMode", "None"),
                "vxlanMode": pool["spec"].get("vxlanMode", "None"),
                "natOutgoing": pool["spec"].get("natOutgoing", False)
            }
            for pool in ip_pools["items"]
        ]
        return {"status": "success", "response": ip_pool_list}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}


def create_ip_pool(name, cidr, ipip_mode="Always", vxlan_mode="Never", nat_outgoing=True):
    """
    Create a new IP Pool in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    ip_pool = {
        "apiVersion": "crd.projectcalico.org/v1",
        "kind": "IPPool",
        "metadata": {
            "name": name
        },
        "spec": {
            "cidr": cidr,
            "ipipMode": ipip_mode,
            "vxlanMode": vxlan_mode,
            "natOutgoing": nat_outgoing
        }
    }
    try:
        response = custom_api.create_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools",
            body=ip_pool
        )
        return {"status": "success", "response": response}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def get_ip_pool_details(name):
    """
    Get details of a specific IP Pool in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        ip_pool = custom_api.get_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools",
            name=name
        )
        return {"status": "success", "response": ip_pool}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def update_ip_pool(name, updates):
    """
    Update information related to an IP Pool in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        response = custom_api.patch_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools",
            name=name,
            body=updates
        )
        return {"status": "success", "response": response}
    except client.exceptions.ApiException as e:
        print(e)
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def delete_ip_pool(name):
    """
    Delete a specific IP Pool in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        response = custom_api.delete_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools",
            name=name,
            body=client.V1DeleteOptions()
        )
        return {"status": "success", "response": response}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def monitor_ip_pool_usage():
    """
    Monitor IP Pool usage and metrics in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        ip_pools = custom_api.list_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools"
        )
        usage_metrics = []
        for pool in ip_pools["items"]:
            pool_name = pool["metadata"]["name"]
            cidr = pool["spec"]["cidr"]
            # Example metric: number of allocated IPs
            allocated_ips = custom_api.list_cluster_custom_object(
                group="crd.projectcalico.org",
                version="v1",
                plural="blockaffinities",
                label_selector=f"projectcalico.org/namespace={pool_name}"
            )
            usage_metrics.append({
                "name": pool_name,
                "cidr": cidr,
                "allocated_ips": len(allocated_ips["items"])
            })
        return {"status": "success", "response": usage_metrics}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    
def assign_ip_pool_to_namespace(namespace, ip_pool_name):
    """
    Assign a Calico IP Pool to a Kubernetes namespace.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        # Patch the namespace with the IP Pool annotation
        patch_body = {
            "metadata": {
                "annotations": {
                    "cni.projectcalico.org/ipv4pools": f'["{ip_pool_name}"]'
                }
            }
        }
        response = custom_api.patch_namespaced_custom_object(
            group="v1",
            version="v1",
            namespace=namespace,
            plural="namespaces",
            name=namespace,
            body=patch_body
        )
        return {"status": "success", "response": response}
    except client.exceptions.ApiException as e:
        print(e)
        return {"status": "error", "error": str(e.reason), "error-status": e.status}

def assign_ip_pool_to_pod(namespace, pod_name, ip_pool_name):
    """
    Assign a Calico IP Pool to a Kubernetes pod based on labels.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        # Patch the pod with the IP Pool annotation
        patch_body = {
            "metadata": {
                "annotations": {
                    "cni.projectcalico.org/ipv4pools": f'["{ip_pool_name}"]'
                }
            }
        }
        response = custom_api.patch_namespaced_custom_object(
            group="v1",
            version="v1",
            namespace=namespace,
            plural="pods",
            name=pod_name,
            body=patch_body
        )
        return {"status": "success", "response": response}
    except client.exceptions.ApiException as e:
        print(e)
        return {"status": "error", "error": str(e.reason), "error-status": e.status}
    

def calculate_ip_pool_metrics(cidr, allocated_ips):
    """
    Calculate total IPs, used IPs, and free IPs for a given CIDR and allocated IPs.
    """
    network = ipaddress.ip_network(cidr)
    total_ips = network.num_addresses
    used_ips = len(allocated_ips)
    free_ips = total_ips - used_ips
    return total_ips, used_ips, free_ips

def get_ip_pool_metrics():
    """
    Get metrics for each IP Pool in Kubernetes using Calico.
    """
    _, _, _, custom_api = load_custom_kubeconfig()
    try:
        ip_pools = custom_api.list_cluster_custom_object(
            group="crd.projectcalico.org",
            version="v1",
            plural="ippools"
        )
        metrics = []
        for pool in ip_pools["items"]:
            pool_name = pool["metadata"]["name"]
            cidr = pool["spec"]["cidr"]
            # Example metric: number of allocated IPs
            allocated_ips = custom_api.list_cluster_custom_object(
                group="crd.projectcalico.org",
                version="v1",
                plural="blockaffinities",
                label_selector=f"projectcalico.org/namespace={pool_name}"
            )
            total_ips, used_ips, free_ips = calculate_ip_pool_metrics(cidr, allocated_ips["items"])
            metrics.append({
                "name": pool_name,
                "cidr": cidr,
                "total_ips": total_ips,
                "used_ips": used_ips,
                "free_ips": free_ips
            })
        return {"status": "success", "response": metrics}
    except client.exceptions.ApiException as e:
        return {"status": "error", "error": str(e.reason), "error-status": e.status}