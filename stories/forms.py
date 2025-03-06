import threading
from django import forms
from django.contrib.auth import get_user_model
from stories.models import Review
User = get_user_model()

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    class Meta:
        model = Review
        fields = (
            'subject', 'comment', 'rate'
        )
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'comment': forms.TextInput(attrs={'placeholder': 'Comment'}),
            'rate': forms.TextInput(attrs={'placeholder': 'Rate'}),
        }