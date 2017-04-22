from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .lists import *
from django.core.exceptions import ValidationError

class User_Login_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(User_Login_Form, self).__init__(*args, **kwargs)
    class Meta:
        model = User
        fields = ['email', 'password']
        exclude =['last_name', 'sex', 'is_admmin', 'avatar', 'birthday', 'city']
        widgets = {
        'email': forms.EmailInput(attrs={'type':'email', 'class':'input', 'id':'login_email', 'required':'required', 'placeholder':'Email'}),
        'password': forms.PasswordInput(attrs={'type':'password', 'class':'input', 'id':'login_password', 'required':'required', 'placeholder':'password'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError(
            ('User %(value)s doesnt exist.'),
            params={'value': email},)
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean(self):
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError('The password field was blank.')
        try:
            login = self.cleaned_data['email']
        except KeyError:
            raise forms.ValidationError('The email field was blank.')

        return self.cleaned_data


class User_Registration_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(User_Registration_Form, self).__init__(*args, **kwargs)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password', 'class':'input', 'id':'reg_password2', 'required':'required', 'placeholder':'password'}))
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'last_name', 'sex', 'birthday', 'city']
        exclude =['is_admmin' 'avatar',]
        widgets = {
        'email': forms.EmailInput(attrs={'type':'email', 'class':'input', 'id':'reg_email', 'required':'required', 'placeholder':'Email'}),
        'password': forms.PasswordInput(attrs={'type':'password', 'class':'input', 'id':'reg_password', 'required':'required', 'placeholder':'password'}),
        'name': forms.TextInput(attrs={'type':'text', 'class':'input', 'id':'reg_name', 'placeholder':'name'}),
        'last_name': forms.TextInput(attrs={'type':'text', 'class':'input', 'id':'reg_last_name', 'placeholder':'last_name'}),
        'birthday': forms.TextInput(attrs={'type':'date', 'class':'input', 'id':'reg_birthday', 'placeholder':'birthday'}),
        'sex': forms.RadioSelect(attrs={}, choices=SEX_LIST,),
        'avatar': forms.FileInput(attrs={'type':'file', 'class':'input', 'id':'reg_avatar', 'placeholder':'avatar'}),
        'city': forms.TextInput(attrs={'type':'text', 'class':'input','required':'required', 'id':'reg_city', 'placeholder':'city'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(
            ('Email %(value)s already in use.'),
            params={'value': email},)
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password", None)
        password2 = self.cleaned_data.get("password2", None)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
            ("Passwords doesn't match."),
            params={'value': password2},)
        return password2


    def clean(self):
        try:
            name = self.cleaned_data['name']
        except KeyError:
            raise forms.ValidationError('The name field was blank.')
        try:
            sex = self.cleaned_data['sex']
        except KeyError:
            raise forms.ValidationError('The sex field was blank.')
        try:
            city = self.cleaned_data['city']
        except KeyError:
            raise forms.ValidationError('The city field was blank.')
        return self.cleaned_data
