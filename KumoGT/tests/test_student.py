from django.test import TestCase

from ..models import Student

    
class Student_TestCase(TestCase):
    
    def setUp(self):
        Student.objects.create(first_name='Jack', last_name='Davis', uin='000000001', email='000001@gmail.com', gender='male')
        Student.objects.create(first_name='Rose', last_name='Davis', uin='000000002', email='000002@gmail.com', gender='female')
        
    def test_student(self):
        jack = Student.objects.get(first_name='Jack')
        rose = Student.objects.get(first_name='Rose')
        self.assertEqual(jack.uin, '000000001')
        self.assertEqual(jack.email, '000001@gmail.com')
        self.assertEqual(jack.gender, 'male')
        self.assertEqual(rose.uin, '000000002')
        self.assertEqual(rose.email, '000002@gmail.com')
        self.assertEqual(rose.gender, 'female')