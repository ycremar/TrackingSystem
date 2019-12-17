from django.shortcuts import render, redirect

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import HttpResponse

from .models import Deg_Plan_Doc, Student, Degree, Session_Note,\
    Annual_Review_Doc, Qual_Exam_Doc
from django.core.exceptions import ObjectDoesNotExist

from .forms import create_doc_form, deg_form, session_note_form

import re

from django.contrib.auth.decorators import user_passes_test

def permission_check(request, model, option = ''):
    perm_type = {'del':'delete', 'del_all':'delete', 'add':'add', None:'change', 'ch':'change'}
    if request.user.has_perm("KumoGT.{0}_{1}".format(perm_type[option], model._meta.model_name)):
        return True
    else: return False

def get_stu_search_dict(args, need_form = False):
    text_fields = ["uin", "first_name", "last_name", "advisor"]
    seach_dict = {}
    if need_form: search_form_params = {}
    for name, val in args.items():
        if val:
            if need_form: search_form_params[name] = val
            if name == 'cur_degree': 
                if val == 'none':
                    seach_dict[name] = None
                    continue
                else:
                    name += '__deg_type'
            if name in text_fields:
                seach_dict[name + "__contains"] = val
            else:
                seach_dict[name] = val
    if need_form: return [seach_dict, search_form_params]
    else: return seach_dict

def delete(request, model, id, obj_text, field_text, show_field, redirect_url):
    try:
        del_obj = model.objects.get(id = id)
    except ObjectDoesNotExist:
        messages.error(request, obj_text + "does not exist.")
        return redirect(redirect_url)
    else:
        attr = re.match( r'^@(.+)$', field_text)
        if attr: field_text = "{0}".format(del_obj.__dict__[attr.group()[1:]])
        if field_text != "": field_text += ": "
        if request.method == 'POST':
            if hasattr(del_obj, "get_{0}_display".format(show_field)):
                show_field_text = getattr(del_obj, "get_{0}_display".format(show_field))
                msg_text = "({0}{1}) is deleted.".format(field_text, show_field_text())
            else:
                msg_text = "({0}{1}) is deleted.".format(field_text, del_obj.__dict__[show_field])
            del_obj.delete()
            messages.success(request, obj_text + msg_text)
            return redirect(redirect_url)
        else:
            if hasattr(del_obj, "get_{0}_display".format(show_field)):
                show_field_text = getattr(del_obj, "get_{0}_display".format(show_field))
                text = "Are you sure to delete this " + obj_text.lower() + \
                    "({0}{1})?".format(field_text, show_field_text())
            else:
                text = "Are you sure to delete this " + obj_text.lower() + \
                    "({0}{1})?".format(field_text, del_obj.__dict__[show_field])
            text += "<br><br>This change CANNOT be recovered."
            return render(request, 'confirmation.html', {
                'confirm_message': mark_safe(text),
                'redirect_url': redirect_url,
                })

def delete_record(request, degree_id, info_model, doc_model, record_text, redirect_url):
    if info_model: info = info_model.objects.filter(degree__id = degree_id)
    else: info = None
    docs = doc_model.objects.filter(degree__id = degree_id)
    if not docs.exists() and (not info or not info.exists()):
        messages.error(request, "This record does not exist.")
        return redirect(redirect_url)
    else:
        degree = Degree.objects.get(id = degree_id)
        if request.method == 'POST':
            msg_text = " record(UIN: {0}, degree: {1}, first registered at {2} {3}) is deleted.".format\
                    (degree.stu.uin, degree.get_deg_type_display(), degree.first_reg_sem, degree.first_reg_year)
            if info and info.exists(): info.delete()
            if docs.exists(): docs.delete()
            messages.success(request, record_text + msg_text)
            return redirect(redirect_url)
        else:
            text = "Are you sure to delete this " + record_text + \
                    " record(UIN: {0}, degree: {1}, first registered at {2} {3})?".format\
                    (degree.stu.uin, degree.get_deg_type_display(), degree.first_reg_sem, degree.first_reg_year)
            text += "<br>All documents and information in this record will be deleted."
            text += "<br><br>This change CANNOT be recovered."
            return render(request, 'confirmation.html', {
                'confirm_message': mark_safe(text),
                'redirect_url': redirect_url,
                })

def post_deg_doc(request, record_text, doc_model, redirect_url, deg_id, option, id, type_widget,\
    info_model = None, info_form = None, extra_fields = []):
    forms = []
    changed, error = False, False
    # submit info form
    if info_form:
        if info_form.has_changed():
            changed = True
            if info_form.is_valid():
                info = info_form.save(commit = False)
                info.degree = Degree.objects.get(id = deg_id)
                info.save()
            else:
                error = True
                messages.error(request, mark_safe("Information of {0} fail to update due to:<br>{1}".format\
                    (record_text, info_form.errors)))
    # submit doc forms
    docs = doc_model.objects.all() if deg_id == '0' else doc_model.objects.filter(degree_id = deg_id)
    for doc in docs:
        forms.append(create_doc_form(doc_model, type_widget, extra_fields)(request.POST, request.FILES,\
            instance = doc, prefix = str(doc.id)))
    for form in forms:
        if form.has_changed():
            changed = True
            if form.is_valid():
                doc = form.save(commit = False)
                doc.degree = Degree.objects.get(id = deg_id)
                doc.save()
            else:
                error = True
                messages.error(request, mark_safe("{0}({1}) fail to update due to:<br>{2}".format\
                    (form.instance.doc, form.instance.get_doc_type_display(), form.errors)))
    # submit new doc form
    if option == 'add' and deg_id != '0':
        new_form = create_doc_form(doc_model, type_widget, extra_fields)(request.POST, request.FILES, prefix = 'new')
        changed = True
        if new_form.is_valid():
            doc = new_form.save(commit = False)
            doc.degree = Degree.objects.get(id = deg_id)
            doc.save()
        else:
            error = True
            messages.error(request, mark_safe("{0}({1}) fail to update due to:<br>{2}".format\
                (new_form.instance.doc, new_form.instance.get_doc_type_display(), new_form.errors)))
    # deal with msgs
    if not changed: messages.info(request, "Noting is changed.")
    elif not error:
        info_msg = " and information " if info_form else ""
        messages.success(request, "Documents" + info_msg + "are updated.")
    else:
        info_msg = " or information " if info_form else ""
        messages.warning(request, "Some documents" + info_msg + "are not updated.")
    return ['submit', redirect("/degree/" + deg_id + redirect_url)]

def deg_doc(request, record_text, doc_model, redirect_url, deg_id, option, id,\
    info_model = None, info_form = None, extra_fields = []):
    if option == 'del':
        return ['del', delete(request, doc_model, id, "Document", "@doc",\
            "doc_type", "/degree/" + deg_id + redirect_url)]
    if option == 'del_all':
        return ['del_all', delete_record(request, deg_id, info_model, doc_model, record_text,\
            "/degree/" + deg_id + redirect_url)]
    type_widget = 1 if record_text == "Other Document" else 0
    if request.method == 'POST':
        return post_deg_doc(request, record_text, doc_model, redirect_url, deg_id, option, id, type_widget,\
            info_model, info_form, extra_fields)
    else:
        docs = doc_model.objects.all() if deg_id == '0' else doc_model.objects.filter(degree_id = deg_id)
        forms = []
        for doc in docs:
            forms.append(create_doc_form(doc_model, type_widget, extra_fields)(instance = doc, prefix = str(doc.id)))
        # form for new document
        if option == 'add' and deg_id != '0':
            forms.append(create_doc_form(doc_model, type_widget, extra_fields)(prefix = 'new'))
        deg = Degree.objects.get(id = deg_id) if deg_id != '0' else None
        return ['show', [deg, forms]]

def get_info_form(request, deg_id, info_model, info_form_class):
    if deg_id != '0':
        info = info_model.objects.filter(degree__id = deg_id)
        if info.exists(): 
            info = info.get()
            if request.method == 'POST': info_form = info_form_class(request.POST, instance = info, prefix = "info")
            else: info_form = info_form_class(instance = info, prefix = "info")
        else:
            if request.method == 'POST': info_form = info_form_class(request.POST, prefix = "info")
            else: info_form = info_form_class(prefix = "info")
    else: info_form = None
    return info_form

def get_stu_objs(model, form, stu_id, option = '', form_needed = True):
    objs = model.objects.all() if stu_id == '0' else model.objects.filter(stu_id = stu_id)
    student = Student.objects.get(id = stu_id) if stu_id != '0' else None
    if form_needed:
        forms = []
        for obj in objs:
            forms.append(form(instance = obj, prefix = str(obj.id)))
        if option == 'add' and stu_id != '0':
            forms.append(form(prefix = 'new'))
        return [forms, student]
    else:
        new_form = form(prefix = 'new') if option == 'add' and stu_id != '0' else None
        return [objs, student, new_form]

def post_degrees(request, stu_id, option = '', id = 0):
    forms = []
    degrees = Degree.objects.all() if stu_id == '0' else Degree.objects.filter(stu_id = stu_id)
    changed, error = False, False
    for degree in degrees:
        forms.append(deg_form(request.POST, instance = degree, prefix = str(degree.id)))
    for form in forms:
        if form.has_changed():
            changed = True
            if form.is_valid():
                if form.instance.deg_type != 'phd' and\
                    (Annual_Review_Doc.objects.filter(degree_id = form.instance.id)\
                    or Qual_Exam_Doc.objects.filter(degree_id = form.instance.id)):
                    error = True
                    err_text = "All annual review and qualifying exam records must be deleted before changing this degree to non-PhD degrees!"
                    messages.error(request,\
                        mark_safe("Degree({0} first registered at {1} {2}) failed to update due to:<br>{3}".format\
                            (form.instance.get_deg_type_display(), form.instance.get_first_reg_sem_display(),\
                            form.instance.first_reg_year, err_text)))
                else:
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
            new_form = deg_form(request.POST, prefix = 'new')
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
    if not changed: messages.info(request, 'Noting is changed.')
    elif not error: messages.success(request, 'Degrees are updated.')
    else: messages.warning(request, 'Some degrees are not updated.')
    return redirect('degrees', stu_id = stu_id)

def post_session_note(request, stu_id, option = '', id = 0):
    changed, error = False, False
    if stu_id != '0':
        student = Student.objects.get(id = stu_id)
        if option == 'add':
            changed = True
            new_form = session_note_form(request.POST, prefix = 'new')
            if new_form.is_valid():
                note = new_form.save(commit = False)
                note.stu = student
                note.save()
            else:
                error = True
                messages.error(request,\
                    mark_safe("Session note({0} first registered at {1} {2}) failed to update due to:<br>{3}".format\
                        (new_form.instance.get_deg_type_display(), new_form.instance.get_first_reg_sem_display(),\
                            new_form.instance.first_reg_year, new_form.errors)))
    if not changed: messages.info(request, 'Noting is changed.')
    elif not error: messages.success(request, 'Session notes are updated.')
    else: messages.warning(request, 'Some session notes are not updated.')
    return redirect('session_note', stu_id = stu_id)