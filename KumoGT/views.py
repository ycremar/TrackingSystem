from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import login_required
from django.views.static import serve

from .models import Deg_Plan_Doc
from .forms import create_doc_form, search_form
from .crypt import Cryptographer

from django.core.exceptions import ObjectDoesNotExist

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
    
def degree_plan(request, option = '', id = 0):
    if request.method == 'POST':
        forms = []
        deg_plans = Deg_Plan_Doc.objects.all()
        changed, error = False, False
        for deg_plan in deg_plans:
            forms.append(create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES,\
                instance = deg_plan, prefix = str(deg_plan.id)))
        for form in forms:
            if form.has_changed():
                changed = True
                if form.is_valid():
                    form.save()
                else:
                    error = True
                    messages.error(request, mark_safe("{0} ({1}) failed to update due to:<br>{2}".format\
                        (form.instance.doc, form.instance.doc_type, form.errors)))
        if option == 'add' :
            new_form = create_doc_form(Deg_Plan_Doc)(request.POST, request.FILES, prefix = 'new')
            if new_form.is_valid():
                changed = True
                new_form.save()
        if not changed:
            messages.info(request, 'Noting is changed.')
        elif not error:
            messages.success(request, 'Documents are updated.')
        else:
            messages.warning(request, 'Some documents are not updated.')
        return redirect('degree_plan')
    elif request.method == 'GET':
        if option == 'del':
            try:
                del_doc = Deg_Plan_Doc.objects.get(id = id)
                os.remove(del_doc.doc.path)
            except ObjectDoesNotExist:
                messages.error(request, 'Document does not exist.')
            except OSError as err:
                err_text = "{0}".format(err)
                messages.error(request, err_text[err_text.find(']') + 1 : err_text.find(':')])
            else:
                del_doc.delete()
                messages.success(request, 'Document is deleted.')
            return redirect('degree_plan')
        forms = []
        deg_plans = Deg_Plan_Doc.objects.all()
        if deg_plans.count() == 0 and option != 'add': return redirect('degree_plan', option = 'add')
        for deg_plan in deg_plans:
            forms.append(create_doc_form(Deg_Plan_Doc)(instance = deg_plan, prefix = str(deg_plan.id)))
        if option == 'add' :
            forms.append(create_doc_form(Deg_Plan_Doc)(prefix = 'new'))
        return render(request, 'degree_plan.html', {
            'forms': forms,
            'option': option,
        })
    
    
# @login_required
def serve_protected_document(request, file_path):

    file_path = os.path.join(settings.BASE_DIR, file_path)
    try:
        with open(file_path, 'rb') as fh:
            content = Cryptographer.decrypted(fh.read())
            response = HttpResponse(content, content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    except:
        raise Http404
        
def search(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('') #needs update
    else:
        form = search_form()
    return render(request, 'search.html', {'form': form})
