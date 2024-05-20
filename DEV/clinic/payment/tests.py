from django.test import TestCase
from clinic.tests import BaseTestCase

# Create your tests here.
class testPaymentMethods(BaseTestCase):
    
    def testFirstOption(self):
        response = self.client.get("/payment/1/")
        print(response.content)
