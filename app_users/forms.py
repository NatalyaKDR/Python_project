from django.forms import ModelForm
from .models import UserComment

class CommentForm(ModelForm):
    class Meta:
        model=UserComment
        fields=['text', 'item']
