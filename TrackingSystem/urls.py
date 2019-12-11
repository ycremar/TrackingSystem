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
from KumoGT.registration import sign_up, manage_users, all_users, manage_my_account,\
    change_my_pwd, change_users_pwd, delete_user, activate_user, deactivate_user
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

stu_search_options = r'(?:uin=(?P<uin>[0-9]+)/)?'\
                     r'(?:first_name=(?P<first_name>[a-zA-Z]+)/)?'\
                     r'(?:last_name=(?P<last_name>[a-zA-Z]+)/)?'\
                     r'(?:gender=(?P<gender>[a-zA-Z_]+)/)?'\
                     r'(?:ethnicity=(?P<ethnicity>[a-zA-Z_]+)/)?'\
                     r'(?:us_residency=(?P<us_residency>[a-zA-Z]+)/)?'\
                     r'(?:texas_residency=(?P<texas_residency>[a-zA-Z]+)/)?'\
                     r'(?:citizenship=(?P<citizenship>[a-zA-Z]+)/)?'\
                     r'(?:status=(?P<status>[a-zA-Z]+)/)?'\
                     r'(?:start_year=(?P<start_year>[0-9-]+)/)?'\
                     r'(?:start_sem=(?P<start_sem>[a-zA-Z]+)/)?'\
                     r'(?:cur_degree=(?P<cur_degree>[a-zA-Z_]+)/)?'\
                     r'(?:cur_degree__major=(?P<cur_degree__major>[a-zA-Z]+)/)?'\
                     r'(?:advisor=(?P<advisor>[a-zA-Z ]+)/)?'\
                     r'(?:upe=(?P<upe>[yesno]+)/)?'\
                     r'(?:ace=(?P<ace>[yesno]+)/)?'\
                     r'(?:iga=(?P<iga>[yesno]+)/)?$'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Admin and users authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('account/', manage_my_account, name='account'),
    path('account/change_pwd/', change_my_pwd, name='change_my_pwd'),
    path('manage_users/', manage_users, name='manage_users'),
    path('manage_users/sign_up/', sign_up, name='sign_up'),
    path('manage_users/user_list/', all_users, name='user_list'),
    path('manage_users/user_list/change_pwd/<int:id>/', change_users_pwd, name='change_users_pwd'),
    path('manage_users/user_list/delete_user/<int:id>/', delete_user, name='delete_user'),
    path('manage_users/user_list/activate/<int:id>/', activate_user, name='activate_user'),
    path('manage_users/user_list/deactivate/<int:id>/', deactivate_user, name='deactivate_user'),
    path('admin/', admin.site.urls, name='admin'),

    re_path(r'^download_stu_info/' + stu_search_options,\
        views.download_stu_info, name = 'download_stu_info'),
    re_path(r'^get_tmp_file/(?:type=(?P<content_type>.+)/)(?:path=(?P<file_path>.+))$',\
        views.get_tmp_file, name = 'get_tmp_file'),

    re_path(r'^students/' + stu_search_options\
        , views.students, name = 'students'),
    #path('students/', views.students, name = 'students'),
    path('students/edit/<int:id>/', views.edit_stu, name = 'edit_stu'),
    path('students/delete/<int:id>/', views.delete_stu, name = 'delete_stu'),
    path('students/add/', views.create_stu, name = 'create_stu'),

    re_path(r'^student/(?:(?P<stu_id>\d+)/)degrees/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.degrees, name = 'degrees'),
    re_path(r'^student/(?:(?P<stu_id>\d+)/)session_notes/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.session_notes, name = 'session_notes'),

    path('upload/', views.upload, name='upload'),
    path('form_upload/', views.form_upload, name='form_upload'),
    # degree docs    
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)degree_plan/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.degree_plan, name = 'degree_plan'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)preliminary_exam/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.preliminary_exam, name = 'preliminary_exam'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)qualifying_exam/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.qualifying_exam, name = 'qualifying_exam'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)annual_review/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.annual_review, name = 'annual_review'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)thesis_dissertation_proposal/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.thesis_dissertation_proposal, name = 'thesis_dissertation_proposal'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)final_exam/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.final_exam, name = 'final_exam'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)thesis_dissertation/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.thesis_dissertation, name = 'thesis_dissertation'),
    re_path(r'^degree/(?:(?P<deg_id>\d+)/)other_doc/(?:(?P<option>[a-z_]+)/)?(?:(?P<id>\d+)/)?$',\
        views.other_doc, name = 'other_doc'),

    re_path(r"^(?P<file_path>.+)$", views.serve_protected_document, name='decrypt_and_serve'),
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
