from django import forms
from .models import *


class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'email', 'name', 'website']
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type Your Comment'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['website'].widget.attrs['placeholder'] = 'Website'
