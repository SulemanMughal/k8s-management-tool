from django.urls import path

from .views import index,list_nodes,describe_node,cordon_node,uncordon_node,drain_node,get_node_pod_cidr_view

urlpatterns = [
    path("", index, name="index"),
    path('nodes/list/', list_nodes, name='list_nodes'),
    path('nodes/describe/<str:node_name>/', describe_node, name='describe_node'),
    path('nodes/cordon/<str:node_name>/', cordon_node, name='cordon_node'),
    path('nodes/uncordon/<str:node_name>/', uncordon_node, name='uncordon_node'),
    path('nodes/drain/<str:node_name>/', drain_node, name='drain_node'),
    path("get-node-pod-cidr/", get_node_pod_cidr_view, name="get-node-pod-cidr"),


]