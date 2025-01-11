from django.contrib import admin
from django.urls import path, include 


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("master_app.urls")),
    path("", include("authentication.urls")),
    path("pods/", include("pod_management.urls")),
    path("monitoring", include("monitoring.urls")),
    # path("security-context", include("security_context_app.urls")),
    path("service-management/", include("service_management_app.urls")),
    path("secrets-management/", include("secrets_management_app.urls")),
    path("replicasets-management/", include("replicasets_management.urls")),
    path("deployments-management/", include("deployment_management_app.urls")),
    path("daemonset-management/", include("daemonset_management.urls")),
    path("namespaces-management/", include("namespaces_management_app.urls")),
    path("events-management/", include("events_management_app.urls")),
]




if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)