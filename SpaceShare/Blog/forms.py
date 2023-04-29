from typing import Any
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Newsletter as NewsletterModel, User as UserModel, Post as PostModel, Comment as CommentModel


class NewsletterForm(forms.ModelForm):
    field_order = ['name', 'surname', 'email']

    class Meta:
        model = NewsletterModel
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


class UserRegisterForm(forms.ModelForm):
    c_password = forms.CharField(label="Confirm Password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary',
            'placeholder': 'Confirm Password'
        }))
    field_order = ['login', 'password', 'c_password', 'nickname', 'email']

    class Meta:
        model = UserModel
        exclude = ['slug', 'image', 'description']
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

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
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


class UserLoginForm(forms.Form):
    login = forms.CharField(label="Login", validators=[RegexValidator(
        "^(?=.*?[a-zA-Z\d])[a-zA-Z][a-zA-Z\d_-]{2,28}[a-zA-Z\d]$", message="Login must be between 4 and 30 characters long and must start with a letter and end with a letter or number. It can contain a floor and dash between the start and end.")], widget=forms.TextInput(attrs={
            'class': 'form-control border border-secondary',
            'placeholder': 'Login'
        }))
    password = forms.CharField(label="Password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary',
            'placeholder': 'Confirm Password'
        }))
    field_order = ['login', 'password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': '3',
                'class': "form-control form-control-sm",
                'placeholder': "Your comment..."
            })
        }
        error_messages = {
            'content': {
                'min_length': ("Comment should be minimum 2 characters long."),
                'max_length': ("Comment should be maximum 2000 characters long.")
            }
        }

    def save(self, user, post, commit=True):
        comment = super().save(commit=False)
        comment.user = UserModel.objects.get(nickname=user)
        comment.post = PostModel.objects.get(slug=post)
        if commit:
            comment.save()
        return comment


class ChangeEmailForm(forms.Form):
    old_email = forms.EmailField(label="New E-mail", validators=[RegexValidator(
        "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", message="Incorrect expression of e-mail.")], widget=forms.EmailInput({
            'class': 'form-control border border-secondary mb-2',
            'placeholder': 'New E-mail'
        }))
    new_email = forms.EmailField(label="New E-mail", validators=[RegexValidator(
        "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", message="Incorrect expression of e-mail.")], widget=forms.EmailInput({
            'class': 'form-control border border-secondary mb-2',
            'placeholder': 'New E-mail'
        }))
    field_order = ['old_email', 'new_email']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary mb-2',
            'placeholder': 'Old password'
        }))
    new_password = forms.CharField(label="New password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary',
            'placeholder': 'New password'
        }))
    field_order = ['old_password', 'new_password']


class ChangeImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-lg',
    }))


class ChangeDescriptionForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '8',
        'class': "form-control form-control-sm",
        'placeholder': "Your profile description..."
    }))


class DeleteAccountForm(forms.Form):
    password = forms.CharField(label="Old password", validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")], widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-secondary mb-2',
            'placeholder': 'Your password'
        }))
