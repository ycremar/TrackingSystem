from django import forms
from .models import Document
from django.utils import timezone

def create_doc_form(model_in):
    '''Generate Model Form for docs dynamically'''
    class Meta:
        model = model_in        # model input
        fields = ['doc_type', 'doc', 'notes', 'appr_cs_date', 'appr_ogs_date']
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'w3-select'}),
            'notes': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
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
