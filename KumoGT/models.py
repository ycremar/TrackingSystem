from django.db import models
from .crypt_fields import EncryptedFileField

DOCUMENT_TYPE = [('not sel', 'Not Selected'),\
                 ('degree plan', 'Degree Plan'),\
                 ('annual review', 'Annual Review'),\
                 ('other', 'Other')]

DEGREE_PLAN_DOC_TYPE = [('not sel', 'Not Selected'),\
                        ('deg plan', 'Degree Plan'),\
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

DEGREE_TYPE = [('phd', 'PhdCS'),\
               ('ms', 'MsCS'),\
               ('meng', 'MengCS')]

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

class Degree(models.Model):
    deg_type = models.CharField(max_length=255, choices=DEGREE_TYPE, default='none')
    first_reg_year = models.SmallIntegerField(blank = False, default=0, verbose_name='First Registered Year')
    first_reg_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='First Registered Semester')
    last_reg_year = models.SmallIntegerField(blank = False, default=0, verbose_name='Last Registered Year')
    last_reg_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='Last Registered Semester')
    deg_recv_year = models.SmallIntegerField(blank = False, default=0, verbose_name='Degree Received Year')
    deg_recv_sem = models.CharField(max_length=255, choices=SEMESTER_TYPE,\
        default='fall', verbose_name='Degree Received Semester')
    stu = models.ForeignKey(Student, models.CASCADE, null=True, verbose_name='Student')

class Document(models.Model):
    doc = EncryptedFileField(upload_to='documents/', verbose_name='Document')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    appr_cs_date = models.DateField(blank=True, null = True, verbose_name='Aprroved CS') # Approved CS Date
    appr_ogs_date = models.DateField(blank=True, null = True, verbose_name='Aprroved OGS') # Approved OGS Date
    notes = models.CharField(max_length=511, blank=True, verbose_name='Notes')
    degree = models.ForeignKey(Degree, models.CASCADE, null=True)
    class Meta:
        abstract = True

class Deg_Plan_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=DEGREE_PLAN_DOC_TYPE, default='not sel')

class Pre_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=PRE_EXAM_DOC_TYPE, default='not sel')

class Pre_Exam_Info():
    date = models.DateField(verbose_name='Prelim Date')
    result = models.CharField(max_length=255, choices=EXAM_RESULT_TYPE, default='none')
    degree = models.OneToOneField(Degree, models.CASCADE)

class T_D_Prop_Doc(Document): # Thesis/Dissertation Proposal Document
    doc_type = models.CharField(max_length=255, choices=T_D_PROP_DOC_TYPE, default='not sel')

class T_D_Doc(Document): # Thesis/Dissertation Document
    doc_type = models.CharField(max_length=255, choices=T_D_DOC_TYPE, default='not sel')

class T_D_Info():
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    degree = models.OneToOneField(Degree, models.CASCADE)

class Fin_Exam_Doc(Document):
    doc_type = models.CharField(max_length=255, choices=FIN_EXAM_DOC_TYPE, default='not sel')

class Fin_Exam_Info():
    date = models.DateField()
    time = models.TimeField()
    result = models.CharField(max_length=255, choices=EXAM_RESULT_TYPE, default='none')
    title = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=255, blank=True)
    abstract = models.CharField(max_length=1023, blank=True)
    degree = models.OneToOneField(Degree, models.CASCADE)

