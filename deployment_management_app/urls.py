from django.urls import path
from .views import create_deployment_view, monitor_deployment_view, update_deployment_view, delete_deployment_view

urlpatterns = [
    path('deployments/create/<str:namespace>/', create_deployment_view, name='create_deployment'),
    path('deployments/status/<str:namespace>/<str:name>/', monitor_deployment_view, name='monitor_deployment'),
    path('deployments/update', update_deployment_view, name='update_deployment'),
    path('deployments/delete', delete_deployment_view, name='delete_deployment'),
    
]
