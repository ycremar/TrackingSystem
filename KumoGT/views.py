from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.static import serve

from .models import Deg_Plan_Doc, Student, Degree, Pre_Exam_Doc, Pre_Exam_Info,\
    T_D_Prop_Doc, Fin_Exam_Info, Fin_Exam_Doc, T_D_Doc, T_D_Info, Session_Notes
from django.core.paginator import Paginator

from .forms import create_doc_form, stu_search_form, stu_bio_form, deg_form,\
    pre_exam_info_form, final_exam_info_form, thesis_dissertation_info_form, session_notes_form
from .crypt import Cryptographer
from .functions import delete, deg_doc, get_info_form, get_stu_objs, post_degrees, post_session_notes

import os

def conditional_decorator(dec, condition):
    def decorator(func):
        if not condition:
            return func
        return dec(func)
    return decorator

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def home(request):
    docs = Deg_Plan_Doc.objects.all()
    return render(request, 'home.html', { 'docs': docs })

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
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
    
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
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

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def degree_plan(request, deg_id, option = '', id = 0):
    if request.method == 'POST':
        return deg_doc(request, "Degree Plan", Deg_Plan_Doc, "/degree_plan/", deg_id, option, id)[1]
    else:
        method, data = deg_doc(request, "Degree Plan", Deg_Plan_Doc, "/degree_plan/", deg_id, option, id)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'degree_plan.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
            })

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def preliminary_exam(request, deg_id, option = '', id = 0):
    info_form = get_info_form(request, deg_id, Pre_Exam_Info, pre_exam_info_form)
    if request.method == 'POST':
        return deg_doc(request, "Preliminary Exam", Pre_Exam_Doc, "/preliminary_exam/",\
            deg_id, option, id, Pre_Exam_Info, info_form)[1]
    else:
        method, data = deg_doc(request, "Preliminary Exam", Pre_Exam_Doc, "/preliminary_exam/",\
            deg_id, option, id, Pre_Exam_Info)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'preliminary_exam.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
                'info_form': info_form,
            })

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def thesis_dissertation_proposal(request, deg_id, option = '', id = 0):
    if request.method == 'POST':
        return deg_doc(request, "Thesis/Dissertation Proposal", T_D_Prop_Doc, "/thesis_dissertation_proposal/",\
            deg_id, option, id)[1]
    else:
        method, data = deg_doc(request, "Thesis/Dissertation Proposal", T_D_Prop_Doc, "/thesis_dissertation_proposal/",\
            deg_id, option, id)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'thesis_dissertation_proposal.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
            })

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def final_exam(request, deg_id, option = '', id = 0):
    info_form = get_info_form(request, deg_id, Fin_Exam_Info, final_exam_info_form)
    if request.method == 'POST':
        return deg_doc(request, "Final Exam", Fin_Exam_Doc, "/final_exam/",\
            deg_id, option, id, Fin_Exam_Info, info_form)[1]
    else:
        method, data = deg_doc(request, "Final Exam", Fin_Exam_Doc, "/final_exam/",\
            deg_id, option, id, Fin_Exam_Info)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'final_exam.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
                'info_form': info_form,
            })
            
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def thesis_dissertation(request, deg_id, option = '', id = 0):
    info_form = get_info_form(request, deg_id, T_D_Info, thesis_dissertation_info_form)
    if request.method == 'POST':
        return deg_doc(request, "Thesis/Dissertation", T_D_Doc, "/thesis_dissertation/",\
            deg_id, option, id, T_D_Info, info_form)[1]
    else:
        method, data = deg_doc(request, "Thesis/Dissertation", T_D_Doc, "/thesis_dissertation/",\
            deg_id, option, id, T_D_Info)
        if method != 'show': return data
        else:
            deg, forms = data
            return render(request, 'thesis_dissertation.html', {
                'deg': deg,
                'forms': forms,
                'option': option,
                'info_form': info_form,
            })
            
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def session_notes(request, stu_id, option = '', id = 0):
    if option == 'del':
        return delete(request, Session_Notes, id, "Session Note", "advised at",\
            "date", "/student/" + stu_id + "/session_notes/")
    if request.method == 'POST':
        return post_session_notes(request, stu_id, option, id)
    else:
        notes, student, new_form = get_stu_objs(Session_Notes, session_notes_form, stu_id, option, False)
        return render(request, 'session_notes.html', {
            'stu': student,
            'notes': notes,
            'new_form': new_form,
            'option': option,
        })

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
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

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def students(request, **kwargs):# uin, first_name, last_name, gender, status, cur_degree):
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
        
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def create_stu(request, back_url = None):
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
            
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def edit_stu(request, id, back_url = None):
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
            
@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def delete_stu(request, id):
    return delete(request, Student, id, "Student", 'UIN', 'uin', '/students/')

@conditional_decorator(login_required(login_url='/login/'), not settings.DEBUG)
def degrees(request, stu_id, option = '', id = 0):
    if option == 'del':
        return delete(request, Degree, id, "Degree", "",\
            "deg_type", "/student/" + stu_id + "/degrees/", True)
    if request.method == 'POST':
        return post_degrees(request, stu_id, option, id)
    else:
        forms, student = get_stu_objs(Degree, deg_form, stu_id, option)
        cur_deg_id = student.cur_degree.id if student and student.cur_degree else -1
        return render(request, 'degrees.html', {
            'stu': student,
            'cur_deg_id': cur_deg_id,
            'forms': forms,
            'option': option,
        })