from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import FileResponse, HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.views.static import serve

from .models import Deg_Plan_Doc
from .forms import create_doc_form

import os

def home(request):
    docs = Deg_Plan_Doc.objects.all()
    return render(request, 'home.html', { 'docs': docs })

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')
    
def form_upload(request):
    if request.method == 'POST':
        form = create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = create_doc_form(Deg_Plan_Doc)
    return render(request, 'form_upload.html', {
        'form': form
    })
    
def degree_plan(request, option = ''):
    if request.method == 'POST':
        forms = []
        deg_plans = Deg_Plan_Doc.objects.all()
        for deg_plan in deg_plans:
            forms.append(create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES,\
                instance = deg_plan, prefix = str(deg_plan.id)))
        for form in forms:
            if form.is_valid():
                form.save()
        if option == 'add' :
            new_form = create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES, prefix = 'new')
            if new_form.is_valid():
                new_form.save()
        return redirect('degree_plan')
    elif request.method == 'GET':
<<<<<<< HEAD
        forms = []
        uploaded_ats = []
        deg_plans = Deg_Plan_Doc.objects.all()
        if deg_plans.count() == 0 and option != 'add': return redirect('degree_plan', option = 'add')
        for deg_plan in deg_plans:
            forms.append(create_doc_form(Deg_Plan_Doc)(instance = deg_plan, prefix = str(deg_plan.id)))
            uploaded_ats.append(deg_plan.uploaded_at)
        if option == 'add' :forms.append(create_doc_form(Deg_Plan_Doc)(prefix = 'new'))
        table_elements = zip(forms, uploaded_ats)
        return render(request, 'degree_plan.html', {
            'table_elements': table_elements,
            'option': option,
        })
=======
        
        form = create_doc_form(Deg_Plan_Doc)()
    return render(request, 'degree_plan.html', {
        'form': form
    })
    
    
# @login_required
def serve_protected_document(request, file):

    file_path = os.path.join(settings.MEDIA_ROOT, 'documents', file)
    try:
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    except:
        raise Http404
    
>>>>>>> 243e889... serve files through views
