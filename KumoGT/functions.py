from django.shortcuts import render, redirect

from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import Deg_Plan_Doc, Student, Degree
from django.core.exceptions import ObjectDoesNotExist

from .forms import create_doc_form

import re

def delete(request, model, id, obj_text, field_text, show_field, redirect_url, has_choices = False):
    try:
        del_obj = model.objects.get(id = id)
    except ObjectDoesNotExist:
        messages.error(request, obj_text + "does not exist.")
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

def deg_doc(request, doc_model, redirect_url, deg_id, option, id):
    if request.method == 'POST':
        if option == 'del':
            return delete(request, doc_model, id, "Document", "@doc",\
                "doc_type", "/degree/" + deg_id + redirect_url, True)
        forms = []
        changed, error = False, False
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
                    messages.error(request, mark_safe("{0}({1}) failed to update due to:<br>{2}".format\
                        (form.instance.doc, form.instance.get_doc_type_display(), form.errors)))
        if option == 'add' and deg_id != '0':
            new_form = create_doc_form(doc_model)(request.POST, request.FILES, prefix = 'new')
            changed = True
            if new_form.is_valid():
                doc = new_form.save(commit = False)
                doc.degree = Degree.objects.get(id = deg_id)
                doc.save()
            else:
                error = True
                messages.error(request, mark_safe("{0}({1}) failed to update due to:<br>{2}".format\
                    (new_form.instance.doc, new_form.instance.get_doc_type_display(), new_form.errors)))
        if not changed:
            messages.info(request, 'Noting is changed.')
        elif not error:
            messages.success(request, 'Documents are updated.')
        else:
            messages.warning(request, 'Some documents are not updated.')
        return redirect("/degree/" + deg_id + redirect_url)
    else:
        if option == 'del':
            return ['del', delete(request, doc_model, id, "Document", "@doc",\
                "doc_type", "/degree/" + deg_id + redirect_url, True)]
        docs = doc_model.objects.all() if deg_id == '0' else doc_model.objects.filter(degree_id = deg_id)
        if docs.count() == 0 and option != 'add': return ['add', redirect("/degree/" + deg_id + redirect_url + "add/")]
        forms = []
        for doc in docs:
            forms.append(create_doc_form(doc_model)(instance = doc, prefix = str(doc.id)))
        if option == 'add' and deg_id != '0':
            forms.append(create_doc_form(doc_model)(prefix = 'new'))
        deg = Degree.objects.get(id = deg_id) if deg_id != '0' else None
        return ['show', [deg, forms]]