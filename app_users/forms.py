from django.forms import ModelForm, forms
from .models import UserComment

class CommentForm(ModelForm):
    class Meta:
        model=UserComment
        fields=['text', 'author', ]

# class UserForm(forms.Form):
#     username=forms.CharField()
#     password=forms.CharField(widget=forms.PasswordInput)


# class UpdateFile(forms.Form): #загрузка файла
#     title=forms.CharField(max_length=50)
#     file=forms.FileField()
#
#
