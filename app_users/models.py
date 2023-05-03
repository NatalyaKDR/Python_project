from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Item(models.Model):
    title=models.CharField('Заголовок', max_length=50)
    content=models.TextField('Описание', blank=True)
    is_published=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserComment(models.Model):
    text = models.TextField('Описание')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    item=models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Тема комментария", related_name="usercomments_item")
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария", blank=True, null=True)
    status=models.BooleanField(verbose_name="Видимость комментария", default=True)

    def __str__(self):
        return self.text
