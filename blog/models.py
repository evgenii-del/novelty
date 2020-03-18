from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField



class News(models.Model):
    title = models.CharField(max_length=100)
    text = RichTextUploadingField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

class Rate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cours = models.FloatField(default=0)

    def __str__(self):
        return self.name
