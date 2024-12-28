from django.urls import path
from .views import list_replicasets_view

urlpatterns = [
    path('replicasets/<str:namespace>', list_replicasets_view, name='list_replicasets'),
]

