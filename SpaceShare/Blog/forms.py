from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from .models import User


class UserForm(forms.ModelForm):
    c_password = forms.CharField(label="Confirm Password", validators=[RegexValidator(
        "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,30}$", message="Incorrect expression of confirm password.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary',
            'placeholder': 'Confirm Password'
        }))
    field_order = ['login', 'password', 'c_password', 'nickname', 'email']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        c_password = cleaned_data.get("c_password")
        if password != c_password:
            raise forms.ValidationError({
                'password': 'Passwords do not match!',
                'c_password': 'Passwords do not match!'
            })
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(user.password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        exclude = ['image']
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'form-control border border-secondary',
                'placeholder': 'Login'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control border border-secondary',
                'placeholder': 'Password'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control border border-secondary',
                'placeholder': 'Nickname'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border border-secondary',
                'placeholder': 'E-mail'
            })
        }
