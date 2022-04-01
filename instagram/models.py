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