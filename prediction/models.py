from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, default='img')
    image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.title
