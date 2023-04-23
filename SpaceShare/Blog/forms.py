from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Newsletter, User


class NewsletterForm(forms.ModelForm):
    field_order = ['name', 'surname', 'email']

    class Meta:
        model = Newsletter
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'First Name'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'E-mail'
            })
        }

    def send_email(self, email, name, surname):
        html_mail = render_to_string('Blog/emails/newsletter.html', {
            'name': name,
            'surname': surname
        })
        send_mail(
            "SpaceShare - subscribed to the newsletter!",
            "You have subscribed to the newsletter. It is not you? Please contact SpaceShare administration.",
            "newsletter@spaceshare.com",
            [email],
            fail_silently=True,
            html_message=html_mail)


class UserForm(forms.ModelForm):
    c_password = forms.CharField(label="Confirm Password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
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
