from django.db import models
from .crypt_fields import EncryptedFileField

DOCUMENT_TYPE = [('not seleted', 'Not Selected'), \
                 ('degree plan', 'Degree Plan'), \
                 ('annual review', 'Annual Review'),\
                 ('other', 'Other')]

DEGREE_PLAN_DOC_TYPE = [('not sel', 'Not Selected'), \
                        ('deg plan', 'Degree Plan'), \
                        ('other', 'Other')]

PRE_EXAM_DOC_TYPE = [('not sel', 'Not Selected'), \
                     ('checklist', 'Preliminary Exam Checklist'), \
                     ('report', 'Preliminary Exam Report'), \
                     ('written', 'Preliminary Exam Written')]

T_D_PROP_DOC_TYPE = [('not sel', 'Not Selected'), \
                     ('title page', 'Thesis/Dissertation Proposal Title Page'), \
                     ('prop', 'Thesis/Dissertation Proposal')]

T_D_DOC_TYPE = [('not sel', 'Not Selected'), \
                ('approval', 'Thesis/Dissertation Approval Page'), \
                ('t_d', 'Thesis/Dissertation')]

FIN_EXAM_DOC_TYPE = [('not sel', 'Not Selected'), \
                     ('request', 'Request for Final Examination'), \
                     ('req for exemp', 'Request for exemption from Final Examination'), \
                     ('report', 'Report of Final Exam')]

GENDER = [('not seleted', 'Not Selected'), \
          ('male', 'Male'),\
          ('female', 'Female')]

DEGREE_TYPE = [('phd', 'PhdCS'),\
               ('ms', 'Master')]
class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=False)
    uin = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)
    gender = models.CharField(max_length=255, choices=GENDER, default='not sel')


class Document(models.Model):
    doc = EncryptedFileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    appr_cs_date = models.DateField(blank=True, null = True) # Approved CS Date
    appr_ogs_date = models.DateField(blank=True, null = True) # Approved OGS Date
    notes = models.CharField(max_length=511, blank=True)
    student = models.ForeignKey(Student, models.CASCADE, null=True)
    class Meta:
        abstract = True

class Deg_Plan_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=DEGREE_PLAN_DOC_TYPE, default='not sel')

class Pre_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=PRE_EXAM_DOC_TYPE, default='not sel')

class Pre_Exam_Info():
    date = models.DateField()
    result = models.BooleanField()
    student = models.OneToOneField(Student, models.CASCADE)

class T_D_Prop_Doc(Document): # Thesis/Dissertation Proposal Document
    doc_type = models.CharField(max_length=255, choices=T_D_PROP_DOC_TYPE, default='not sel')

class T_D_Doc(Document): # Thesis/Dissertation Document
    doc_type = models.CharField(max_length=255, choices=T_D_DOC_TYPE, default='not sel')

class T_D_Info():
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    student = models.OneToOneField(Student, models.CASCADE)

class Fin_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=FIN_EXAM_DOC_TYPE, default='not sel')

class Fin_Exam_Info():
    date = models.DateField()
    time = models.TimeField()
    result = models.BooleanField()
    title = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=255, blank=True)
    abstract = models.CharField(max_length=1023, blank=True)
    student = models.OneToOneField(Student, models.CASCADE)

