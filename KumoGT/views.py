from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import login_required
from django.views.static import serve

from .models import Deg_Plan_Doc, Student, Degree, Pre_Exam_Doc
from django.core.paginator import Paginator

from .forms import create_doc_form, stu_search_form, stu_bio_form, deg_form, pre_exam_info_form
from .crypt import Cryptographer
from .functions import delete, deg_doc

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
    
def degree_plan(request, deg_id, option = '', id = 0):
    if request.method == 'POST':
        return deg_doc(request, Deg_Plan_Doc, "/degree_plan/", deg_id, option, id)
    else:
        method, data = deg_doc(request, Deg_Plan_Doc, "/degree_plan/", deg_id, option, id)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'degree_plan.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
            })
    
def preliminary_exam(request, deg_id, option = '', id = 0):
    if request.method == 'POST':
        info_form = pre_exam_info_form(request.POST)
        if info_form.is_valid():
            pass
        return deg_doc(request, Pre_Exam_Doc, "/preliminary_exam/", deg_id, option, id)
    else:
        method, data = deg_doc(request, Pre_Exam_Doc, "/preliminary_exam/", deg_id, option, id)
        if method != 'show': return data
        else:
            info_form = pre_exam_info_form()
            deg, forms = data
            return render(request, 'preliminary_exam.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
                'info_form': info_form,
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
        
def students(request, **kwargs):# uin, first_name, last_name, gender, cur_degree):
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
        paginator = Paginator(students, 15) # Show 15 students per page. Use 1 for test.
        page = request.GET.get('page')
        students_page = paginator.get_page(page)
        page = 1 if not page else int(page)
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

def degrees(request, stu_id, option = '', id = 0):
    if request.method == 'POST':
        if option == 'del':
            return delete(request, Degree, id, "Degree", "",\
                "deg_type", "/student/" + stu_id + "/degrees/", True)
        forms = []
        degrees = Degree.objects.all() if stu_id == '0' else Degree.objects.filter(stu_id = stu_id)
        changed, error = False, False
        for degree in degrees:
            forms.append(deg_form(request.POST, request.FILES,\
                instance = degree, prefix = str(degree.id)))
        for form in forms:
            if form.has_changed():
                changed = True
                if form.is_valid():
                    form.save()
                else:
                    error = True
                    messages.error(request,\
                        mark_safe("Degree({0} first registered at {1} {2}) failed to update due to:<br>{3}".format\
                            (form.instance.get_deg_type_display(), form.instance.get_first_reg_sem_display(),\
                                form.instance.first_reg_year, form.errors)))
        if stu_id != '0':
            student = Student.objects.get(id = stu_id)
            current = int(request.POST['current'])
            if option == 'add':
                changed = True
                new_form = deg_form(request.POST, request.FILES, prefix = 'new')
                if new_form.is_valid():
                    degree = new_form.save(commit = False)
                    degree.stu = student
                    degree.save()
                    if current == 0: current = degree.id
                else:
                    error = True
                    messages.error(request,\
                        mark_safe("Degree({0} first registered at {1} {2}) failed to update due to:<br>{3}".format\
                            (new_form.instance.get_deg_type_display(), new_form.instance.get_first_reg_sem_display(),\
                                new_form.instance.first_reg_year, new_form.errors)))
            if current > 0 and (not student.cur_degree or student.cur_degree.id != current):
                student.cur_degree = Degree.objects.get(id = current)
                student.save()
                changed = True
            elif current == -1 and student.cur_degree:
                student.cur_degree = None
                student.save()
                changed = True
        if not changed:
            messages.info(request, 'Noting is changed.')
        elif not error:
            messages.success(request, 'Documents are updated.')
        else:
            messages.warning(request, 'Some documents are not updated.')
        return redirect('degrees', stu_id = stu_id)
    else:
        if option == 'del':
            return delete(request, Degree, id, "Degree", "",\
                "deg_type", "/student/" + stu_id + "/degrees/", True)
        degrees = Degree.objects.all() if stu_id == '0' else Degree.objects.filter(stu_id = stu_id)
        if degrees.count() == 0 and option != 'add': return redirect('degrees', stu_id = stu_id, option = 'add')
        forms = []
        for degree in degrees:
            forms.append(deg_form(instance = degree, prefix = str(degree.id)))
        if option == 'add' and stu_id != '0':
            forms.append(deg_form(prefix = 'new'))
        student = Student.objects.get(id = stu_id) if stu_id != '0' else None
        cur_deg_id = student.cur_degree.id if student and student.cur_degree else -1
        return render(request, 'degrees.html', {
            'stu': student,
            'cur_deg_id': cur_deg_id,
            'forms': forms,
            'option': option,
        })