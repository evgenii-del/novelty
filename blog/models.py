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
    img = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    count = models.PositiveIntegerField(default=0)
    favourite = models.ManyToManyField(User, related_name="favourite", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Rate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cours = models.FloatField(default=0)

    def __str__(self):
        return self.name
