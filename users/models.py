from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='user_images')

    def __str__(self):
        return f'Профайл {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.img.path)

        if image.width > 256 or image.height > 256:
            resize = (256,256)
            image.thumbnail(resize)
            image.save(self.img.path)
