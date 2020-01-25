from django.db import models


class FeedBack(models.Model):
    name = models.CharField('Имя', max_length=120)
    email = models.EmailField('Почта', max_length=120)
    phone = models.CharField('Телефон', max_length=120)
    description = models.TextField('Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форма обратной связи'
        verbose_name_plural = 'Формы обратной связи'
