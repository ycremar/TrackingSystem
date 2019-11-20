from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',\
        widget = forms.TextInput(attrs = {'class': 'w3-input w3-center'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',\
        widget = forms.TextInput(attrs = {'class': 'w3-input w3-center'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',\
        widget = forms.EmailInput(attrs = {'class': 'w3-input w3-center'}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs = {'class': 'w3-input w3-center'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs = {'class': 'w3-input w3-center'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None,\
        widget=forms.Select(attrs = {'class': 'w3-select w3-center'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group',)
        widgets = {
            'username': forms.TextInput(attrs = {'class': 'w3-input w3-center'}),
        }
        
class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs = {'class': 'w3-input w3-center'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs = {'class': 'w3-input w3-center'}),
    )
