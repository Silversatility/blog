from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating and validating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']