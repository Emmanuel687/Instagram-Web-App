from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.

# Image models properties
class Image(models.Model):
    image = CloudinaryField('image', default='')
    name = models.CharField(max_length = 30,default='')
    caption = models.TextField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
# Image models Methods    
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

# Profile Models properties
class Profile(models.Model):
    profile_photo=CloudinaryField('image')
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
# Profile Models methods
    def __str__(self):
        return self.user.username

    def update(self):
        self.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

# Like Model properties
class Like(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.likes

# Comment Model properties
class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)

    def save_comment(self):
        self.save()

    def __str__(self):
        return self.comment