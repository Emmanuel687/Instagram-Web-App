from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    image = CloudinaryField('image', default='')
    name = models.CharField(max_length = 30,default='')
    caption = models.TextField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')

    
    def __str__(self):
        return self.name

    @classmethod
    def search_by_name(cls, search_term):
        images = cls.objects.filter(
            image_name_contains=search_term)
        return images
    
    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()
    
    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()