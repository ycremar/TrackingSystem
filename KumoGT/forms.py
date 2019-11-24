from django import forms
from django.utils import timezone
from .models import Student, Degree, Pre_Exam_Info, Fin_Exam_Info, T_D_Info, Session_Notes,\
    DEGREE_TYPE, STUDENT_STATUS_TYPE, GENDER, SEMESTER_TYPE

class stu_search_form(forms.Form):
    uin = forms.CharField(label = 'UIN', max_length = 255, required = False,\
        widget = forms.TextInput(attrs = {'class': 'w3-input'}))
    first_name = forms.CharField(label = 'First Name', max_length = 255, required = False,\
        widget = forms.TextInput(attrs = {'class': 'w3-input'}))
    last_name = forms.CharField(label = 'Last Name', max_length = 255, required = False,\
        widget = forms.TextInput(attrs = {'class': 'w3-input'}))
    gender = forms.ChoiceField(choices = [('', 'All')] + GENDER, required = False,\
        widget = forms.Select(attrs = {'class': 'w3-select'}))
    status = forms.ChoiceField(choices = [('', 'All')] + STUDENT_STATUS_TYPE, required = False,\
        widget = forms.Select(attrs = {'class': 'w3-select'}))
    cur_degree = forms.ChoiceField(choices = [('', 'All')] + DEGREE_TYPE + [('none', 'None')], required = False,\
        widget = forms.Select(attrs = {'class': 'w3-select'}))
    cur_degree__first_reg_year = forms.IntegerField(max_value = 32767, min_value = -32768, required = False,\
        widget = forms.NumberInput(attrs = {'class': 'w3-input w3-cell w3-center', 'style': 'width:50%'}))
    cur_degree__first_reg_sem = forms.ChoiceField(choices = [('', 'All')] + SEMESTER_TYPE, required = False,\
        widget = forms.Select(attrs = {'class': 'w3-select w3-cell', 'style': 'width:50%'}))
    
class stu_bio_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['uin', 'first_name', 'middle_name', 'last_name', 'email', 'gender', 'status']
        widgets = {
            'uin': forms.TextInput(attrs = {'class': 'w3-input'}),
            'first_name': forms.TextInput(attrs = {'class': 'w3-input w3-light-gray'}),
            'middle_name': forms.TextInput(attrs = {'class': 'w3-input'}),
            'last_name': forms.TextInput(attrs = {'class': 'w3-input w3-light-gray'}),
            'email': forms.EmailInput(attrs = {'class': 'w3-input'}),
            'gender': forms.Select(attrs = {'class': 'w3-select w3-light-gray'}),
            'status': forms.Select(attrs = {'class': 'w3-select'}),
        }

class deg_form(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['deg_type', 'first_reg_year', 'first_reg_sem',\
            'last_reg_year', 'last_reg_sem', 'deg_recv_year', 'deg_recv_sem']
        widgets = {
            'deg_type': forms.Select(attrs = {'class': 'w3-select w3-cell', 'style': 'width: auto;'}),
            'first_reg_year': forms.NumberInput(attrs = {'class': 'w3-input w3-cell', 'style': 'width:38%'}),
            'first_reg_sem': forms.Select(attrs = {'class': 'w3-select w3-cell', 'style': 'width:47%'}),
            'last_reg_year': forms.NumberInput(attrs = {'class': 'w3-input w3-cell', 'style': 'width:38%'}),
            'last_reg_sem': forms.Select(attrs = {'class': 'w3-select w3-cell', 'style': 'width:47%'}),
            'deg_recv_year': forms.NumberInput(attrs = {'class': 'w3-input w3-cell', 'style': 'width:38%'}),
            'deg_recv_sem': forms.Select(attrs = {'class': 'w3-select w3-cell', 'style': 'width:47%'}),
        }

def create_doc_form(model_in):
    '''Generate Model Form for docs dynamically'''
    class Meta:
        model = model_in        # model input
        fields = ['doc_type', 'doc', 'notes', 'appr_cs_date', 'appr_ogs_date']
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'w3-select'}),
            'notes': forms.Textarea(attrs={'cols': 15, 'rows': 5}),
            'appr_cs_date': forms.SelectDateWidget\
                (attrs={'class': 'w3-select'},\
                    years = [y for y in range(timezone.now().year - 7, timezone.now().year + 8)]),
            'appr_ogs_date': forms.SelectDateWidget\
                (attrs={'class': 'w3-select'},\
                    years = [y for y in range(timezone.now().year - 7, timezone.now().year + 8)])
        }

    attrs = {'Meta':Meta}

    _model_form_class = type("DynamicModelForm", (forms.ModelForm,), attrs)     
        # Parameters: object name, tuple(input father)，dict of meta
    
    return _model_form_class    # return a class

class pre_exam_info_form(forms.ModelForm):
    class Meta:
        model = Pre_Exam_Info
        fields = ['date', 'result']
        widgets = {
            'date': forms.SelectDateWidget\
                (attrs={'class': 'w3-select', 'style': 'width:auto'},\
                    years = [y for y in range(timezone.now().year - 7, timezone.now().year + 8)]),
            'result': forms.Select(attrs = {'class': 'w3-select', 'style': 'width:auto;'})
        }

class final_exam_info_form(forms.ModelForm):
    class Meta:
        model = Fin_Exam_Info
        fields = ['date', 'time', 'result', 'title', 'room', 'abstract']
        widgets = {
            'date': forms.SelectDateWidget\
                (attrs={'class': 'w3-select', 'style': 'width:auto'},\
                    years = [y for y in range(timezone.now().year - 7, timezone.now().year + 8)]),
            'result': forms.Select(attrs = {'class': 'w3-select', 'style': 'width:auto;'}),
            'abstract': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'style':"width:80%"}),
            'room': forms.Textarea(attrs={'cols': 50, 'rows': 1, 'style':"width:80%"}),
            'time': forms.TimeInput(attrs={'style':"width:80%"}),
            'title': forms.Textarea(attrs={'cols': 50, 'rows': 1, 'style':"width:80%"}),
        }
        
class thesis_dissertation_info_form(forms.ModelForm):
    class Meta:
        model = T_D_Info
        fields = ['title', 'url']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 50, 'rows': 1, 'style':"width:80%"}),
            'url': forms.URLInput(attrs={'cols': 50, 'rows': 1, 'style':"width:80%"}),
        }
        
class session_notes_form(forms.ModelForm):
    class Meta:
        model = Session_Notes
        fields = ['date', 'note']
        widgets = {
            'date': forms.SelectDateWidget\
                (attrs={'class': 'w3-select', 'style': 'width:auto'},\
                    years = [y for y in range(timezone.now().year - 7, timezone.now().year + 8)]),
            'note': forms.Textarea(attrs={'cols': 50, 'rows': 10, 'style':"width:80%"}),
        }