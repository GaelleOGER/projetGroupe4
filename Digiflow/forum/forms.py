from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Tag


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    username = forms.CharField(max_length=50, required=True)
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

class UserLoginForm(forms.Form):
    username=forms.CharField(label="Nom  d'utilisateur",widget=forms.TextInput(attrs={'placeholder': "Entrer votre nom d'utilisateur"}),max_length=50,required=True)
    password =forms.CharField(label='Mot de passe',widget=forms.PasswordInput(attrs={'placeholder':'Entrer mot de '
                                                                                                   'passe'}),max_length=50,min_length=6,required=True)
    class Meta:
        model= User
        fields=['username','password']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']