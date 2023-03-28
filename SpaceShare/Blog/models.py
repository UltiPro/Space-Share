from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class User(models.Model):
    login = models.CharField(validators=[RegexValidator(
        "^[A-Za-z][A-Za-z0-9_-]{1,13}[A-Za-z0-9]$", message="Incorrect expression of login.")])
    nickname = models.CharField(validators=[RegexValidator(
        "^[a-zA-Z]\w*$", message="Incorrect expression of nickname.")])
    password = models.CharField(validators=[RegexValidator(
        "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,30}$", message="Incorrect expression of password.")])
    email = models.EmailField(validators=[RegexValidator(
        "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", message="Incorrect expression of e-mail.")])

    def __str__(self):
        return self.nickname


class Tag:
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Post(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    title = models.CharField(min_length=3, max_length=150)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    date = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    content = models.TextField(
        validators=[MinLengthValidator(30, MaxLengthValidator(10000))])
    image = models.ImageField(upload_to="posts", null=True)

    def __str__(self):
        return f'{self.title} by {self.author.nickname}'
