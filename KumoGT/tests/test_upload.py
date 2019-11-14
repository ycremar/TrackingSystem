from django.test import TestCase
from django.test.client import RequestFactory

from ..views import *


class Upload_TestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_upload(self):
        request = self.factory.get('/customer/details')
        rt = upload(request)
        self.assertEqual(rt.status_code, 200)