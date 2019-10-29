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
    
def degree_plan(request):
    if request.method == 'POST':
        form = create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    elif request.method == 'GET':
        
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
    