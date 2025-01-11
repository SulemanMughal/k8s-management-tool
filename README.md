#### Pre-reuisites before commit code

- Remove `backports.zoneinfo` from requirements.txt



#### Setup Project

- Get Kubernetes Configuration File Consume Kuberentes-API



#### IP Addresses For the server

- Master Node : 104.131.83.201
- Worker Node-1 : 104.131.43.246
- Worker Node-2 : 104.131.48.221

#### Access Servers through ssh-key

    ssh -i ~/.ssh/new_droplet_key root@104.131.48.221


#### Development Env File

    https://docs.google.com/document/d/19DmsHYfJbxD4EPYLAtKQZsr4CbSloBHWPpp3jmLOQqE/edit?usp=sharing


#### To Install and Configure Postgresql

    https://docs.google.com/document/d/1neeVOj4w_N_7quNffLAbXSHpNnGY9R1qU5s0XZTF1pg/edit?usp=sharing


#### To Test Database Connection:

    python3 ./my_site/test_dbConnection.py


#### To Test Kubernetes API Access:
    python3 ./my_sites/test_access_kube.py



#### First-Time Configure Project

    - python3 -m venv my_env
    - source my_env/bin/activate
    - pip3 install -r requirements.txt
    - python3 manage.py makemigrations
    - python3 manage.py migrate


#### CreateSuperuser

    - python3 manage.py createsuperuser




#### Start A Development Server

    - python3 manage.py runserver

#### Access Web Interface

    - http://localhost:8000



#### Postman to test APIS (gmail : suleman shahid 0087)

    https://web.postman.co/workspace/5f0ba0d3-3614-449e-849c-03018da254e5/request/40942859-fa2250e9-3354-480a-a89f-dc1730819e74


#### Kubernetes Docs Files

    https://drive.google.com/drive/folders/1eKxYTxt1LJqv7AcnAKK1T-8-hA3VQVve


#### Trello Project Management (suleman shahid  : 0087)

    https://trello.com/b/3ZdcZmzj/my-trello-board




#### --------------------------------------------------------------------------------------------


#### Features List:


- Cluster Nodes

    - List Down All Nodes
    - Fetch the podCIDR for a specific node.
    - Describe A Node



- DaemonSet Management

    - Create DaemonSet 
    - Describde
    - List 
    - Update Container Image
    - Delete
    - Get Pods Management By All DaemonSet
    - Get Pods Managed BY A Specific DaemonSet Object
    - DaemonSet with a nodeSelector to restrict it to specific nodes
    - update a DaemonSet with nodeAffinity
    - Mimic pausing a DaemonSet by removing nodeSelector or setting a taint.
    - Resume a DaemonSet by re-adding the nodeSelector.
    - Get the nodes on which a specific DaemonSet is deployed.
    - change the namespace of a DaemonSet.
    - Get the rollout status of a DaemonSet.
    - Get the rollout status of a DaemonSet with periodic polling until the rollout completes.
    - Rollout History Management (Update, Retrieve)
    - Event List For A DaemonSet Object 
    - Update Function to Apply RollingUpdate Strategy

#   template inheritance


# Django : template inheritance


**base.html**


```
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Favicon -->
    <link rel="shortcut icon" href="{% static 'assets/img/favicon.png' %}">


    <title>{% block title %}{% endblock %}</title>

    {% include 'style.html' %}

    {% block extra_style %}
    {% endblock %}



</head>
<body>
    {% block header %}
        {% include 'header.html' %}
    {% endblock %}

    {% block content %}
    {% endblock %}

    {% block footer %}
        {% include 'footer.html' %}
    {% endblock %}

    {% include 'script.html' %}

    {% block extra_script %}
    {% endblock %}


</body>
</html>

```


**index.html**

```
{% extends 'base.html' %}

{% block content %}

<h1>Landing page</h1>


{% endblock %}
```


**app/views.py**

```

def index(request):
    template_name = "master_app/index.html"
    context = {

    }
    return render(request, template_name, context)

```


**app/urls.py**

```
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
]

```


**project/urls.py**

```

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("master_app.urls"))
]



```


**messages.html**

```
{% if messages %}
    {% for message in messages %}
        {% if message.tags == 'error' %}
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
                </button>
            </div>
        {% elif message.tags == 'success' %}
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
                </button>
            </div>
        {% elif message.tags == 'warning' %}
            <div class="alert alert-warning alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
                </button>
            </div>
        {% endif %}
    {% endfor %}
{% endif %}

```

# Django Login Decorator

```
from django.contrib.auth.decorators import login_required

@login_required



```