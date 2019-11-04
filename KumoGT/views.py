from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import login_required
from django.views.static import serve

from .models import Deg_Plan_Doc, Student
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .forms import create_doc_form, stu_search_form, stu_bio_form
from .crypt import Cryptographer


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
    
def delete(request, model, id, obj_text, field_text, show_field, redirect_url):
    try:
        del_obj = model.objects.get(id = id)
    except ObjectDoesNotExist:
        messages.error(request, obj_text + "does not exist.")
    else:
        if request.method == 'POST':
            messages.success(request, obj_text + \
                "({0}: {1}) is deleted.".format(field_text, del_obj.__dict__[show_field]))
            del_obj.delete()
            return redirect(redirect_url)
        else:
            text = "Are you sure to delete this " + obj_text.lower() + \
                "({0}: {1})?".format(field_text, del_obj.__dict__[show_field])
            text += "<br><br>This change CANNOT be recovered."
            return render(request, 'confirmation.html', {
                'confirm_message': mark_safe(text),
                'redirect_url': redirect_url,
                })    

def delete_doc(request, model, id, redirect_url):
    try:
        del_doc = Deg_Plan_Doc.objects.get(id = id)
    except ObjectDoesNotExist:
        messages.error(request, "Document({0}) does not exist.".format(del_doc.doc.name))
        return redirect(redirect_url)
    else:
        if request.method == 'POST':
            try:
                os.remove(del_doc.doc.path)
            except OSError as err:
                err_text = "{0}".format(err)
                messages.error(request, err_text[err_text.find(']') + 1 : err_text.find(':')])
                del_doc.delete()
                messages.warning(request, 'Document is deleted but some errors occur.')
            else:
                del_doc.delete()
                messages.success(request, 'Document is deleted.')
            return redirect(redirect_url)
        else:
            text = "Are you sure to delete this document({0})?".format(del_doc.doc.name)
            text += "<br><br>This change CANNOT be recovered."
            return render(request, 'confirmation.html', {
                'confirm_message': mark_safe(text),
                'redirect_url': redirect_url,
                })    


def degree_plan(request, option = '', id = 0):
    if request.method == 'POST':
        if option == 'del':
            return delete_doc(request, Deg_Plan_Doc, id, "/degree_plan/")
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
    else:
        if option == 'del':
            return delete_doc(request, Deg_Plan_Doc, id, "/degree_plan/")
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
        
def students(request, **kwargs):#, first_name, last_name, gender, cur_degree):
    if request.method == 'POST':
        form = stu_search_form(request.POST)
        form.is_valid()
        redirect_url = '/students/'
        search_form_params = {}
        for name, val in form.cleaned_data.items():
            if val and val != '':
                search_form_params[name] = val
                redirect_url += "{0}={1}/".format(name, val)
        return redirect(redirect_url, **search_form_params)
    else:
        students = Student.objects.all()
        search_form_params = {}
        seach_dict = {}
        for name, val in kwargs.items():
            if val:
                search_form_params[name] = val
                if name == 'cur_degree': 
                    if val == 'none':
                        seach_dict[name] = None
                        continue
                    else:
                        name += '__deg_type'
                seach_dict[name + "__contains"] = val
        if kwargs: students = students.filter(**seach_dict)
        form = stu_search_form(search_form_params)
        paginator = Paginator(students, 1) # Show 1 students per page, 1 is just for test
        page = request.GET.get('page')
        students_page = paginator.get_page(page)
        if not page: page = 1
        else: page = int(page)
        neigh_pages = [n for n in range(max(page - 2, 1), min(page + 3, paginator.num_pages + 1))]
        if len(neigh_pages) == 0 or neigh_pages[0] > 1:
            neigh_pages.insert(0, -1)
            neigh_pages.insert(0, 1)
        if neigh_pages[-1] < paginator.num_pages:
            neigh_pages.append(-1)
            neigh_pages.append(paginator.num_pages)
    return render(request, 'students.html', {
        'form': form,
        'students': students_page,
        'neigh_pages': neigh_pages,
        })
    
def create_stu(request):
    if request.method == 'POST':
        form = stu_bio_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student is added.')
        else: 
            messages.error(request, mark_safe("{0}".format(form.errors)))
        return redirect('create_stu')
    else:
        form = stu_bio_form()
        title = 'Add a Student'
        return render(request, 'stu_bio_info.html', {
            'form': form,
            'title': title,
            })

def edit_stu(request, id):
    if request.method == 'POST':
        form = stu_bio_form(request.POST, instance = Student.objects.get(id = id))
        if form.has_changed():
            if form.is_valid():
                form.save()
                messages.success(request, 'Student is updated.')
            else: 
                messages.error(request, mark_safe("{0}".format(form.errors)))
        else:
            messages.info(request, 'Noting is changed.')
        return redirect('edit_stu', id = id)
    else:
        form = stu_bio_form(instance = Student.objects.get(id = id))
        title = 'Edit Student Bio Info'
        return render(request, 'stu_bio_info.html', {
            'form': form,
            'title': title,
            })

def delete_stu(request, id):
    return delete(request, Student, id, "Student", 'UIN', 'uin', '/students/')