from django.test import TestCase
from .models import Image

# Create your tests here.
class ImageTestCase(TestCase):

    # Set up method
    def setUp(self):
        self.name= Image(name='Manu')

    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.name,Image))
        
    # Testing save method
    def test_save_image(self):
        self.duke.save_image()
        image = Image.objects.all()
        self.assertTrue(len(image) > 0)

    # Test delete method
    def test_delete_image(self,id):
        self.name.delete_image(id='')
        image = Image.objects.all(id)
        self.assertTrue(len(image) == 0)
