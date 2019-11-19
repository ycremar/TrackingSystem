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
from KumoGT.registration import signup, manageusers, all_users
from KumoGT.registration import changepwd, reset_admin_pwd, delete_user, activate_user, deactivate_user
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    
    # Admin and users authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('manageusers/', manageusers, name='manageusers'),
    path('manageusers/signup/', signup, name='signup'),
    path('manageusers/userlist/', all_users, name='userlist'),
    path('manageusers/userlist/resetpwd/<str:usrname>/', reset_admin_pwd, name='reset_pwd'),
    path('manageusers/userlist/changepwd/<str:usrname>/', changepwd, name='change_pwd'),
    path('manageusers/userlist/deleteuser/<str:usrname>/', delete_user, name='delete_user'),
    path('manageusers/userlist/activate/<str:usrname>/', activate_user, name='activate_user'),
    path('manageusers/userlist/deactivate/<str:usrname>/', deactivate_user, name='deactivate_user'),
    path('admin/', admin.site.urls, name='admin'),

    re_path(r'^students/(?:uin=(?P<uin>[0-9]+)/)?'\
        r'(?:first_name=(?P<first_name>[a-zA-Z]+)/)?'
        r'(?:last_name=(?P<last_name>[a-zA-Z]+)/)?'\
        r'(?:gender=(?P<gender>[a-zA-Z]+)/)?'\
        r'(?:status=(?P<status>[a-zA-Z]+)/)?'\
        r'(?:cur_degree=(?P<cur_degree>[a-zA-Z_]+)/)?$',\
        views.students, name = 'students'),
    #path('students/', views.students, name = 'students'),
    path('students/edit/<int:id>/', views.edit_stu, name = 'edit_stu'),
    path('students/delete/<int:id>/', views.delete_stu, name = 'delete_stu'),
    path('students/add/', views.create_stu, name = 'create_stu'),

    re_path(r'student/(?:(?P<stu_id>\d+)/)degrees/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.degrees, name = 'degrees'),

    path('upload/', views.upload, name='upload'),
    path('form_upload/', views.form_upload, name='form_upload'),
    
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)degree_plan/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.degree_plan, name = 'degree_plan'),
        
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)preliminary_exam/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.preliminary_exam, name = 'preliminary_exam'),
        
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)thesis_dissertation_proposal/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.thesis_dissertation_proposal, name = 'thesis_dissertation_proposal'),
        
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)final_exam/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.final_exam, name = 'final_exam'),

    url(r"(?P<file_path>.+)", views.serve_protected_document, name='decrypt_and_serve'),
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
