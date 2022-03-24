from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields=['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email']= forms.EmailField(max_length=150)
        self.fields['username'] = forms.CharField(max_length=100)
        self.fields[ 'password1' ] = forms.CharField(
            strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
            help_text='',
        )
        self.fields[ 'password2' ] = forms.CharField(
            strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
            help_text='',
        )
