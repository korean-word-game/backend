from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from config.utils import get_token
from .models import User
from .managers import UserManager
from .exceptions import SameError, PasswordNotMatchError, DoNotMatchWithTypeError
from django.contrib.auth.hashers import (
    check_password
)


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', )

    def get_user(self):
        uo = User.objects

        user = uo.get(email=self.data.get('username'))

        if check_password(self.data.get('password'), user.password):
            user.token = get_token(user.uuid.urn.__str__())
            user.save()
            return user
        else:
            raise User.DoesNotExist


class TokenLoginForm(forms.Form):
    token = forms.CharField(
        label='Token',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Token',
                'required': 'True',
            }
        )
    )

    def get_user(self, refresh=True):
        uo = User.objects

        user = uo.get(token=self.data.get('token'))
        if refresh:
            user.token = get_token(user.uuid.urn.__str__())
            user.save()
        return user


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise PasswordNotMatchError()
        return password2

    def save(self, commit=True):
        uo = User.objects
        if uo.filter(email=self.data.get('username')).exists():
            raise SameError('이름')

        user = super(RegisterForm, self).save(commit=False)

        user.set_password(self.clean_password2())
        user.token = get_token(user.uuid.urn.__str__())

        if commit:
            user.save()
        return user


# 장고기본
class UserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nickname',
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.token = get_token(user.uuid.urn.__str__())
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password'
    )

    class Meta:
        model = User
        fields = ('password', 'username', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
