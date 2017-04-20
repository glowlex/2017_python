from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .lists import *

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
        #error_messages = {
              #'login': {
        #'required': 'This field is required',
        #'invalid': 'Enter a valid value',},
                #}

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User doesnt exist.')
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
    class Meta:
        model = User
        fields = ['email', 'password','name', 'last_name', 'sex', 'avatar', 'birthday', 'city']
        exclude =['is_admmin']
        widgets = {
        'email': forms.EmailInput(attrs={'type':'email', 'class':'input', 'id':'reg_email', 'required':'required', 'placeholder':'Email'}),
        'password': forms.PasswordInput(attrs={'type':'password', 'class':'input', 'id':'reg_password', 'required':'required', 'placeholder':'password'}),
        'password2': forms.PasswordInput(attrs={'type':'password', 'class':'input', 'id':'reg_password2', 'required':'required', 'placeholder':'password'}),
        'name': forms.TextInput(attrs={'type':'text', 'class':'input', 'id':'reg_name', 'placeholder':'name'}),
        'last_name': forms.TextInput(attrs={'type':'text', 'class':'input', 'id':'reg_last_name', 'placeholder':'last_name'}),
        'birthday': forms.TextInput(attrs={'type':'date', 'class':'input', 'id':'reg_birthday','required':'required', 'placeholder':'birthday'}),
        'sex': forms.RadioSelect(attrs={}, choices=SEX_LIST,),
        'avatar': forms.FileInput(attrs={'type':'file', 'class':'form-control', 'id':'reg_avatar', 'placeholder':'avatar'}),
        }

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.exclude(pk=self.instance.pk).filter(login=login).exists():
            raise forms.ValidationError(u'Login "%s" is already in use.' % login)
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    #def clean_email(self):
    #    from django.core.validators import validate_email
    #    email = self.cleaned_data['email']
    #    try:
        #    validate_email(email)
    #    except:
        #    raise forms.ValidationError('Email is incorect')
    #    return email

    def clean(self):
        #try:
        #    password = self.cleaned_data['password']
        #except KeyError:
        #    raise forms.ValidationError('The password field was blank.')
        #try:
        #    login = self.cleaned_data['login']
        #except KeyError:
        #    raise forms.ValidationError('The login field was blank.')
        #try:
        #    email = self.cleaned_data['email']
        #except KeyError:
        #    raise forms.ValidationError('The email field was blank.')
        #try:
        #    nick = self.cleaned_data['nick']
        #except KeyError:
        #    raise forms.ValidationError('The nick field was blank.')

        return self.cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
