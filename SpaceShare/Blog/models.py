from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify

from .regexes import regex_validator_email, regex_validator_login, regex_validator_password, regex_validator_nickname


class Newsletter(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, validators=[regex_validator_email])

    def __str__(self):
        return f"{self.name} {self.surname}"


class Author(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True, blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    description = models.TextField(
        validators=[MinLengthValidator(15), MaxLengthValidator(2000)], default="Information about author.")
    email = models.EmailField(validators=[regex_validator_email])
    image = models.ImageField(
        upload_to="authors", null=True, default="users/default.png")

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        self.slug = "-".join((slugify(self.name), slugify(self.surname)))
        super().save(*args, **kwargs)


class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class Post(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=False, blank=True)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    content = models.TextField(
        validators=[MinLengthValidator(30), MaxLengthValidator(10000)])
    image = models.ImageField(upload_to="posts", null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class User(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True, blank=True)
    login = models.CharField(unique=True, max_length=15,
                             validators=[regex_validator_login])
    password = models.CharField(max_length=100, validators=[
                                regex_validator_password])
    nickname = models.CharField(unique=True, max_length=15, validators=[
                                regex_validator_nickname])
    email = models.EmailField(unique=True, validators=[regex_validator_email])
    image = models.ImageField(
        upload_to="users", null=True, default="users/default.png")
    description = models.TextField(
        validators=[MinLengthValidator(15), MaxLengthValidator(2000)], default="Information about user.", null=True)

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nickname)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(
        validators=[MinLengthValidator(2), MaxLengthValidator(2000)])

    def __str__(self):
        return f"{self.user.nickname} - {self.post.title}"
