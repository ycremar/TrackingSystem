from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .crypt_fields import EncryptedFileField
from django.dispatch import receiver
import os

DOCUMENT_TYPE = [('not sel', 'Not Selected'),\
                 ('degree plan', 'Degree Plan'),\
                 ('annual review', 'Annual Review'),\
                 ('other', 'Other')]

DEGREE_PLAN_DOC_TYPE = [('not sel', 'Not Selected'),\
                        ('deg plan', 'Degree Plan'),\
                        ('P. change commitee', 'Petition for change of committee'),\
                        ('P. course change', 'Petition for course change'),\
                        ('P. extension of time limits', 'Petition for extension of time limits'),\
                        ('P. waivers of exceptions', 'Petition for waivers of exceptions'),\
                        ('mdd', 'MDD'),\
                        ('other', 'Other')]

PRE_EXAM_DOC_TYPE = [('not sel', 'Not Selected'),\
                     ('checklist', 'Preliminary Exam Checklist'),\
                     ('report', 'Preliminary Exam Report'),\
                     ('written', 'Preliminary Exam Written')]

T_D_PROP_DOC_TYPE = [('not sel', 'Not Selected'),\
                     ('title page', 'Thesis/Dissertation Proposal Title Page'),\
                     ('prop', 'Thesis/Dissertation Proposal')]

T_D_DOC_TYPE = [('not sel', 'Not Selected'),\
                ('approval', 'Thesis/Dissertation Approval Page'),\
                ('t_d', 'Thesis/Dissertation')]

FIN_EXAM_DOC_TYPE = [('not sel', 'Not Selected'),\
                     ('request', 'Request for Final Examination'),\
                     ('req for exemp', 'Request for exemption from Final Examination'),\
                     ('report', 'Report of Final Exam')]

GENDER = [('not sel', 'Not Selected'),\
          ('male', 'Male'),\
          ('female', 'Female')]

STUDENT_STATUS_TYPE = [('current', 'Current'),\
                       ('graduated', 'Gradudated'),\
                       ('invalid', 'Invalid')]

DEGREE_TYPE = [('phd', 'PhDCS'),\
               ('ms_thesis', 'MSCS(Thesis)'),\
               ('ms_non_thesis', 'MSCS(Non-Thesis)'),\
               ('meng', 'MEngCS')]

SEMESTER_TYPE = [('fall', 'Fall'),\
                 ('spring', 'Spring'),\
                 ('summer', 'Summer')]

EXAM_RESULT_TYPE = [('none', '----'),\
                 ('pass', 'Pass'),\
                 ('fail', 'Fail')]

class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=False, verbose_name='First Name')
    middle_name = models.CharField(max_length=255, blank=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=255, blank=False, verbose_name='Last Name')
    uin = models.CharField(max_length=255, blank=False, unique = True, verbose_name='UIN')
    email = models.EmailField(blank=False)
    gender = models.CharField(max_length=255, choices=GENDER, default='not sel')
    cur_degree = models.OneToOneField('Degree', models.SET_NULL, verbose_name='Current Degree', null=True)
    status = models.CharField(max_length=255, choices=STUDENT_STATUS_TYPE, default='current')

class Degree(models.Model):
    deg_type = models.CharField(max_length=255, choices=DEGREE_TYPE, default='none')
    first_reg_year = models.SmallIntegerField(blank = False, default=0, verbose_name='First Registered Year',\
        validators=[MaxValueValidator(32767), MinValueValidator(-32768)])
    first_reg_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='First Registered Semester')
    last_reg_year = models.SmallIntegerField(blank = False, default=0, verbose_name='Last Registered Year',\
        validators=[MaxValueValidator(32767), MinValueValidator(-32768)])
    last_reg_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='Last Registered Semester')
    deg_recv_year = models.SmallIntegerField(blank = False, default=0, verbose_name='Degree Received Year',\
        validators=[MaxValueValidator(32767), MinValueValidator(-32768)])
    deg_recv_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='Degree Received Semester')
    stu = models.ForeignKey(Student, models.CASCADE, verbose_name='Student')

class Document(models.Model):
    doc = EncryptedFileField(upload_to='documents/', verbose_name='Document')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    appr_cs_date = models.DateField(blank=True, null = True, verbose_name='Aprroved CS') # Approved CS Date
    appr_ogs_date = models.DateField(blank=True, null = True, verbose_name='Aprroved OGS') # Approved OGS Date
    notes = models.CharField(max_length=511, blank=True, verbose_name='Notes')
    degree = models.ForeignKey(Degree, models.CASCADE)
    class Meta:
        abstract = True

class Deg_Plan_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=DEGREE_PLAN_DOC_TYPE, default='not sel')

class Pre_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=PRE_EXAM_DOC_TYPE, default='not sel')

class Pre_Exam_Info(models.Model):
    date = models.DateField(verbose_name='Prelim Date')
    result = models.CharField(max_length=255, choices=EXAM_RESULT_TYPE, default='none')
    degree = models.OneToOneField(Degree, models.CASCADE)

class T_D_Prop_Doc(Document): # Thesis/Dissertation Proposal Document
    doc_type = models.CharField(max_length=255, choices=T_D_PROP_DOC_TYPE, default='not sel')

class T_D_Doc(Document): # Thesis/Dissertation Document
    doc_type = models.CharField(max_length=255, choices=T_D_DOC_TYPE, default='not sel')

class T_D_Info(models.Model):
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    degree = models.OneToOneField(Degree, models.CASCADE)

class Fin_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=FIN_EXAM_DOC_TYPE, default='not sel')

class Fin_Exam_Info(models.Model):
    date = models.DateField()
    time = models.TimeField()
    result = models.CharField(max_length=255, choices=EXAM_RESULT_TYPE, default='none')
    title = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=255, blank=True)
    abstract = models.CharField(max_length=1023, blank=True)
    degree = models.OneToOneField(Degree, models.CASCADE)

class Session_Notes(models.Model):
    date = models.DateField()
    note = models.CharField(max_length=4096, blank=True)

@receiver(models.signals.post_delete, sender=Deg_Plan_Doc)
@receiver(models.signals.post_delete, sender=Pre_Exam_Doc)
@receiver(models.signals.post_delete, sender=T_D_Prop_Doc)
@receiver(models.signals.post_delete, sender=T_D_Doc)
@receiver(models.signals.post_delete, sender=Fin_Exam_Doc)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.doc:
        if os.path.isfile(instance.doc.path):
            os.remove(instance.doc.path)

@receiver(models.signals.pre_save, sender=Deg_Plan_Doc)
@receiver(models.signals.pre_save, sender=Pre_Exam_Doc)
@receiver(models.signals.pre_save, sender=T_D_Prop_Doc)
@receiver(models.signals.pre_save, sender=T_D_Doc)
@receiver(models.signals.pre_save, sender=Fin_Exam_Doc)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Document` object is updated
    with new file.
    """
    if not instance.id:
        return False

    try:
        old_file = sender.objects.get(id=instance.id).doc
    except Document.DoesNotExist:
        return False

    new_file = instance.doc
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)