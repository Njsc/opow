# encoding:utf-8
from django import forms
from models import Image, User


class ImgForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_url', 'desc')


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'mobile',)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'required',}),
                               max_length=50, error_messages={"required": '用户名不能为空',})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required',}),
                               max_length=20, error_messages={"required": '密码不能为空',})
