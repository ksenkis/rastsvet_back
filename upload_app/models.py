from django.db import models


class BlackWhiteImage(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return 'image'
