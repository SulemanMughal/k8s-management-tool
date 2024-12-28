from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('nodes/list/', views.list_nodes, name='list_nodes'),
    path('nodes/describe/<str:node_name>/', views.describe_node, name='describe_node'),
    path('nodes/cordon/<str:node_name>/', views.cordon_node, name='cordon_node'),
    path('nodes/uncordon/<str:node_name>/', views.uncordon_node, name='uncordon_node'),
    path('nodes/drain/<str:node_name>/', views.drain_node, name='drain_node'),

]