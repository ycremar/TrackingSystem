from django.db import models

DOCUMENT_TYPE_CHOICES = [('not seleted', 'Not Selected'), \
                         ('degree plan', 'Degree Plan'), \
                         ('annual review', 'Annual Review'),\
                         ('other', 'Other')]

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=255, choices=DOCUMENT_TYPE_CHOICES, default='not seleted')
    uploaded_at = models.DateTimeField(auto_now_add=True)