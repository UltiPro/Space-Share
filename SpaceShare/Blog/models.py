from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify


class Newsletter(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.EmailField(validators=[RegexValidator(
        "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", message="Incorrect expression of e-mail.")])

    def __str__(self):
        return f'{self.name} {self.surname}'


class Author(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.EmailField(validators=[RegexValidator(
        "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", message="Incorrect expression of e-mail.")])
    image = models.ImageField(upload_to="authors", null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Tag(models.Model):
    tag = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="tags", null=False)

    def __str__(self):
        return self.tag


class User(models.Model):
    login = models.CharField(max_length=15, validators=[RegexValidator(
        "^[A-Za-z][A-Za-z0-9_-]{1,13}[A-Za-z0-9]$", message="Incorrect expression of login.")])
    password = models.CharField(max_length=30, validators=[RegexValidator(
        "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,30}$", message="Incorrect expression of password.")])
    nickname = models.CharField(max_length=15, validators=[RegexValidator(
        "^[a-zA-Z]\w*$", message="Incorrect expression of nickname.")])
    email = models.EmailField(validators=[RegexValidator(
        "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", message="Incorrect expression of e-mail.")])
    image = models.ImageField(upload_to="users", null=True)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=False, blank=True)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    content = models.TextField(
        validators=[MinLengthValidator(30, MaxLengthValidator(10000))])
    image = models.ImageField(upload_to="posts", null=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, related_name="post", null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    date = models.DateField(auto_now=True)
    content = models.TextField(
        validators=[MinLengthValidator(30, MaxLengthValidator(2000))])
