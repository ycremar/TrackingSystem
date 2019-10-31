"""TrackingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from KumoGT import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('upload/', views.upload, name='upload'),
    path('form_upload/', views.form_upload, name='form_upload'),
<<<<<<< HEAD
    #path('degree_plan/', views.degree_plan, name = 'degree_plan'),
<<<<<<< HEAD
    re_path(r'^degree_plan/(?:(?P<option>\S+)/)?$', views.degree_plan, name = 'degree_plan')
=======
    path('degree_plan/', views.degree_plan, name = 'degree_plan'),
=======
    re_path(r'^degree_plan/(?:(?P<option>[a-z]+)/)?(?:(?P<id>\d+)/)?$', views.degree_plan, name = 'degree_plan'),
<<<<<<< HEAD
>>>>>>> 9b03c5a... Add function of deleting to degree plan and import some css class and style.
    path('media/documents/<str:file>', views.serve_protected_document, name='serve_protected_document'),
>>>>>>> 243e889... serve files through views
=======
    url(r"(?P<file_path>.+)", views.serve_protected_document, name='decrypt_and_serve'),
>>>>>>> 19a31e4... add file encryption
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)