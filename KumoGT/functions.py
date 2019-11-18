from django.shortcuts import render, redirect

from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import Deg_Plan_Doc, Student, Degree
from django.core.exceptions import ObjectDoesNotExist

from .forms import create_doc_form

import re

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def delete(request, model, id, obj_text, field_text, show_field, redirect_url, has_choices = False):
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
            if has_choices:
                show_field_text = getattr(del_obj, "get_{0}_display".format(show_field))
                msg_text = "({0}{1}) is deleted.".format(field_text, show_field_text())
            else:
                msg_text = "({0}{1}) is deleted.".format(field_text, del_obj.__dict__[show_field])
            del_obj.delete()
            messages.success(request, obj_text + msg_text)
            return redirect(redirect_url)
        else:
            if has_choices:
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

@user_passes_test(lambda u: u.is_superuser)
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

def deg_doc(request, record_text, doc_model, redirect_url, deg_id, option, id, info_model = None, info_form = None):
    if option == 'del':
        return ['del', delete(request, doc_model, id, "Document", "@doc",\
            "doc_type", "/degree/" + deg_id + redirect_url, True)]
    if option == 'del_all':
        return ['del_all', delete_record(request, deg_id, info_model, doc_model, record_text,\
            "/degree/" + deg_id + redirect_url)]
    if request.method == 'POST':
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
            forms.append(create_doc_form(doc_model)(request.POST, request.FILES,\
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
            new_form = create_doc_form(doc_model)(request.POST, request.FILES, prefix = 'new')
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
        if not changed:
            messages.info(request, "Noting is changed.")
        elif not error:
            info_msg = "and information " if info_form else ""
            messages.success(request, "Documents " + info_msg + "are updated.")
        else:
            info_msg = "or information " if info_form else ""
            messages.warning(request, "Some documents " + info_msg + "are not updated.")
        return ['submit', redirect("/degree/" + deg_id + redirect_url)]
    else:
        docs = doc_model.objects.all() if deg_id == '0' else doc_model.objects.filter(degree_id = deg_id)
        forms = []
        for doc in docs:
            forms.append(create_doc_form(doc_model)(instance = doc, prefix = str(doc.id)))
        # form for new document
        if option == 'add' and deg_id != '0':
            forms.append(create_doc_form(doc_model)(prefix = 'new'))
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