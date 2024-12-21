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