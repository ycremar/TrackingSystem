from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, Http404
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import login_required
from django.views.static import serve

from .models import Deg_Plan_Doc
from .forms import create_doc_form
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
        if option == 'del':
            try:
                del_doc = Deg_Plan_Doc.objects.get(id = id)
                os.remove(del_doc.doc.path)
<<<<<<< HEAD
            except:
                raise Http404
            del_doc.delete()
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 9b03c5a... Add function of deleting to degree plan and import some css class and style.
=======
=======
            messages.success(request, 'Document is deleted.')
>>>>>>> 9f356dd... Refine messages in degree plan and small bug fixes.
=======
            except ObjectDoesNotExist:
                messages.error(request, 'Document does not exist.')
            except OSError as err:
                err_text = "{0}".format(err)
                messages.error(request, err_text[err_text.find(']') + 1 : err_text.find(':')])
            else:
                del_doc.delete()
                messages.success(request, 'Document is deleted.')
>>>>>>> 62292a2... Handling of exceptions of deleting a doc and auto scrolling when adding docs.
            return redirect('degree_plan')
>>>>>>> 1720aaa... Add function of messages and fix a bug which leads to vertical scrollbar missing.
        forms = []
        deg_plans = Deg_Plan_Doc.objects.all()
        if deg_plans.count() == 0 and option != 'add': return redirect('degree_plan', option = 'add')
        for deg_plan in deg_plans:
            forms.append(create_doc_form(Deg_Plan_Doc)(instance = deg_plan, prefix = str(deg_plan.id)))
<<<<<<< HEAD
<<<<<<< HEAD
            uploaded_ats.append(deg_plan.uploaded_at)
        if option == 'add' :forms.append(create_doc_form(Deg_Plan_Doc)(prefix = 'new'))
        table_elements = zip(forms, uploaded_ats)
=======
            infos.append({'id': deg_plan.id, 'uploaded_at': deg_plan.uploaded_at})
        if option == 'add' :
            forms.append(create_doc_form(Deg_Plan_Doc)(prefix = 'new'))
            infos.append({'id': 0, 'uploaded_at': ''})
        table_elements = zip(forms, infos)
>>>>>>> 9b03c5a... Add function of deleting to degree plan and import some css class and style.
=======
        if option == 'add' :
            forms.append(create_doc_form(Deg_Plan_Doc)(prefix = 'new'))
>>>>>>> 1720aaa... Add function of messages and fix a bug which leads to vertical scrollbar missing.
        return render(request, 'degree_plan.html', {
            'forms': forms,
            'option': option,
        })
=======
        
        form = create_doc_form(Deg_Plan_Doc)()
    return render(request, 'degree_plan.html', {
        'form': form
    })
    
    
# @login_required
def serve_protected_document(request, file_path):

    # file_path = os.path.join(settings.MEDIA_ROOT, 'documents', file)
    try:
        with open(file_path, 'rb') as fh:
            content = Cryptographer.decrypted(fh.read())
            response = HttpResponse(content, content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    except:
        raise Http404
    
>>>>>>> 243e889... serve files through views
