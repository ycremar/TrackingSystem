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

    re_path(r'^students/(?:uin=(?P<uin>[0-9]+)/)?'\
        r'(?:first_name=(?P<first_name>[a-zA-Z]+)/)?'
        r'(?:last_name=(?P<last_name>[a-zA-Z]+)/)?'\
        r'(?:gender=(?P<gender>[a-zA-Z]+)/)?'\
        r'(?:cur_degree=(?P<cur_degree>[a-zA-Z]+)/)?$',\
        views.students, name = 'students'),
    #path('students/', views.students, name = 'students'),
    path('students/edit/<int:id>/', views.edit_stu, name = 'edit_stu'),
    path('students/delete/<int:id>/', views.delete_stu, name = 'delete_stu'),
    path('students/add/', views.create_stu, name = 'create_stu'),

    path('upload/', views.upload, name='upload'),
    path('form_upload/', views.form_upload, name='form_upload'),
    #path('degree_plan/', views.degree_plan, name = 'degree_plan'),

    re_path(r'^degree_plan/(?:(?P<option>[a-z]+)/)?(?:(?P<id>\d+)/)?$', views.degree_plan, name = 'degree_plan'),

    url(r"(?P<file_path>.+)", views.serve_protected_document, name='decrypt_and_serve'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
