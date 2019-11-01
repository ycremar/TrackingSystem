from django.test import TestCase

from ..crypt import Cryptographer

class CryptographerTestCase(TestCase):
    
    def test_encryption(self):
        data = b"this is test data 1"
        self.assertNotEqual(Cryptographer.encrypted(data), data)
        
    def test_decryption(self):
        data = b"This is test data 2"
        self.assertEqual(
            Cryptographer.decrypted(Cryptographer.encrypted(data)),
            data
        )