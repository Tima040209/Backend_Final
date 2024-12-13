from django.test import TestCase
from tasks import send_email_task
from models import Product

class TaskTestCase(TestCase):
    def test_send_email_task(self):
        result = send_email_task.delay('test@example.com')
        self.assertTrue(result)


class ProductTestCase(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name='Test Product', price=100)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)
