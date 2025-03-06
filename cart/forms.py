import threading
from django import forms
from django.contrib.auth import get_user_model
from cart.models import Cart
User = get_user_model()

class CartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    class Meta:
        model = Cart
        fields = (
            'quantity',
        )
  