from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Newsletter as NewsletterModel, Author as AuthorModel, User as UserModel, Post as PostModel, Comment as CommentModel
from .regexes import regex_validator_email, regex_validator_login, regex_validator_password


class NewsletterForm(forms.ModelForm):
    field_order = ["name", "surname", "email"]

    class Meta:
        model = NewsletterModel
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "First Name"
            }),
            "surname": forms.TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Last Name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "E-mail"
            })
        }

    def send_email(self):
        cleaned_data = super(NewsletterForm, self).clean()
        html_mail = render_to_string("Blog/emails/newsletter.html", {
            "name": cleaned_data.get("name"),
            "surname": cleaned_data.get("surname")
        })
        try:
            send_mail(
                "SpaceShare - subscribed to the newsletter!",
                "You have subscribed to the newsletter. It is not you? Please contact SpaceShare administration.",
                "newsletter@spaceshare.com",
                [cleaned_data.get("email")],
                fail_silently=True,
                html_message=html_mail)
            return True
        except:
            return False


class UserRegisterForm(forms.ModelForm):
    c_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        "class": "form-control border border-secondary",
        "placeholder": "Confirm Password"
    }))
    field_order = ["login", "password", "c_password", "nickname", "email"]

    class Meta:
        model = UserModel
        exclude = ["slug", "image", "description"]
        widgets = {
            "login": forms.TextInput(attrs={
                "class": "form-control border border-secondary",
                "placeholder": "Login"
            }),
            "password": forms.PasswordInput(attrs={
                "class": "form-control border border-secondary",
                "placeholder": "Password"
            }),
            "nickname": forms.TextInput(attrs={
                "class": "form-control border border-secondary",
                "placeholder": "Nickname"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control border border-secondary",
                "placeholder": "E-mail"
            })
        }

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        c_password = cleaned_data.get("c_password")
        if password != c_password:
            raise forms.ValidationError({
                "c_password": "Passwords do not match!"
            })
        try:
            AuthorModel.objects.get(email=cleaned_data.get("email"))
            raise forms.ValidationError({
                "email": "The email you entered is already taken."
            })
        except AuthorModel.DoesNotExist:
            pass
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(user.password)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    login = forms.CharField(label="Login", validators=[regex_validator_login], widget=forms.TextInput(attrs={
        "class": "form-control border border-secondary",
        "placeholder": "Login"
    }))
    password = forms.CharField(label="Password", validators=[regex_validator_password], widget=forms.PasswordInput(attrs={
        "class": "form-control border border-secondary",
        "placeholder": "Confirm Password"
    }))
    field_order = ["login", "password"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": "3",
                "class": "form-control form-control-sm",
                "placeholder": "Your comment..."
            })
        }
        error_messages = {
            "content": {
                "min_length": ("Comment should be minimum 2 characters long."),
                "max_length": ("Comment should be maximum 2000 characters long.")
            }
        }

    def save(self, user, post, commit=True):
        comment = super().save(commit=False)
        comment.user = UserModel.objects.get(nickname=user)
        comment.post = PostModel.objects.get(slug=post)
        comment.content = comment.content.replace("    ", "&emsp;")
        if commit:
            comment.save()
        return comment


class ChangeEmailForm(forms.ModelForm):
    old_email = forms.EmailField(label="New E-mail", validators=[regex_validator_email], widget=forms.EmailInput({
        "class": "form-control border border-secondary mb-2",
        "placeholder": "Old E-mail"
    }))
    field_order = ["old_email", "email"]

    class Meta:
        model = UserModel
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control border border-secondary mb-2",
                "placeholder": "New E-mail"
            })
        }

    def clean(self):
        cleaned_data = super(ChangeEmailForm, self).clean()
        try:
            is_email_occupied_by_user = UserModel.objects.get(
                email=cleaned_data.get("email"))
        except UserModel.DoesNotExist:
            is_email_occupied_by_user = None
        try:
            is_email_occupied_by_author = AuthorModel.objects.get(
                email=cleaned_data.get("email"))
        except AuthorModel.DoesNotExist:
            is_email_occupied_by_author = None
        if cleaned_data.get("old_email") != self.instance.email:
            raise forms.ValidationError({
                "old_email": "The current email address is invalid."
            })
        if cleaned_data.get("old_email") == cleaned_data.get("email"):
            raise forms.ValidationError({
                "email": "The old email cannot be new email."
            })
        if is_email_occupied_by_user or is_email_occupied_by_author:
            raise forms.ValidationError({
                "email": "The email you entered is already taken."
            })
        return cleaned_data


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(label="Old password", validators=[regex_validator_password], widget=forms.PasswordInput(attrs={
        "class": "form-control border border-secondary mb-2",
        "placeholder": "Old password"
    }))
    field_order = ["old_password", "password"]

    class Meta:
        model = UserModel
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(attrs={
                "class": "form-control border border-secondary mb-2",
                "placeholder": "New Password"
            })
        }

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if not check_password(cleaned_data.get("old_password"), self.instance.password):
            raise forms.ValidationError({
                "old_password": "Your current password is incorrect."
            })
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(user.password)
        if commit:
            user.save()
        return user


class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={
                "class": "form-control border border-secondary mb-2",
                "required": True
            })
        }

    def clean(self):
        cleaned_data = super(ChangeImageForm, self).clean()
        if cleaned_data.get("image") == self.instance.image:
            raise forms.ValidationError({
                "image": "This field is required."
            })
        return cleaned_data


class DeleteAccountForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(attrs={
                "class": "form-control border border-danger mb-2",
                "placeholder": "Your Password"
            })
        }

    def clean(self):
        cleaned_data = super(DeleteAccountForm, self).clean()
        if not check_password(cleaned_data.get("password"), self.instance.password):
            raise forms.ValidationError({
                "password": "The password is incorrect."
            })
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.delete()
        return None


class ChangeDescriptionForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": "8",
                "class": "form-control form-control-sm border border-secondary mb-2",
                "placeholder": "Your profile description...",
                "min-length": 15,
                "max-length": 2000
            })
        }
        error_messages = {
            "description": {
                "min_length": ("Description should be minimum 15 characters long."),
                "max_length": ("Description should be maximum 2000 characters long.")
            }
        }

    def save(self, commit=True):
        content = super().save(commit=False)
        content.description = content.description.replace("    ", "&emsp;")
        if commit:
            content.save()
        return content
