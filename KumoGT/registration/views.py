from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group

from .forms import SignUpForm, ChangePasswordForm
from KumoGT.functions import _delete_user


@user_passes_test(lambda u: u.is_superuser)
def manageusers(request):
    return render(request, 'manageusers.html')

@user_passes_test(lambda u: u.is_superuser)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            group = form.cleaned_data.get('group')
            user = authenticate(username=username, password=raw_password)
            group.user_set.add(user)
            return redirect('manageusers')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def all_users(request):
    users = User.objects.all()
    return render(request, 'userlist.html', { 'users': users })
    
@user_passes_test(lambda u: u.is_superuser)
def changepwd(request, usrname):
    user = User.objects.get(username=usrname)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            return redirect('manageusers')
    else:
        form = ChangePasswordForm()
    return render(request, 'changepwd.html', {'form': form, 'username': user.username})
    
@user_passes_test(lambda u: u.is_superuser)
def reset_admin_pwd(request, usrname):
    users = User.objects.all()
    return render(request, 'userlist.html', { 'users': users })
    
@user_passes_test(lambda u: u.is_superuser)
def deactivate_user(request, usrname):
    user = User.objects.get(username=usrname)
    user.is_active = False
    user.save()
    return redirect('userlist')
    
@user_passes_test(lambda u: u.is_superuser)
def activate_user(request, usrname):
    user = User.objects.get(username=usrname)
    user.is_active = True
    user.save()
    return redirect('userlist')
    
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, usrname):
    return _delete_user(request, User, usrname, "User", 'Username', 'username', 'userlist')
    
