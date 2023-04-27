from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify


class Newsletter(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, validators=[RegexValidator(
        "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", message="Incorrect expression of e-mail.")])

    def __str__(self):
        return f'{self.name} {self.surname}'


class Author(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True, blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    description = models.TextField(
        validators=[MinLengthValidator(30), MaxLengthValidator(2000)], default="Information about author")
    email = models.EmailField(validators=[RegexValidator(
        "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", message="Incorrect expression of e-mail.")])
    image = models.ImageField(upload_to="authors", null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class User(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True, blank=True)
    login = models.CharField(unique=True, max_length=15, validators=[RegexValidator(
        "^(?=.*?[a-zA-Z\d])[a-zA-Z][a-zA-Z\d_-]{2,28}[a-zA-Z\d]$", message="Login must be between 4 and 30 characters long and must start with a letter and end with a letter or number. It can contain a floor and dash between the start and end.")])
    password = models.CharField(max_length=100, validators=[RegexValidator(
        "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\]\\;:'\"/,|{}<>?]{8,40}$", message="Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.")])
    nickname = models.CharField(unique=True, max_length=15, validators=[RegexValidator(
        "^[a-zA-Z]\w*$", message="Incorrect expression of nickname.")])
    email = models.EmailField(unique=True, validators=[RegexValidator(
        "^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", message="Incorrect expression of e-mail.")])
    image = models.ImageField(
        upload_to="users", null=True, default="users/default.png")
    description = models.TextField(
        validators=[MinLengthValidator(15), MaxLengthValidator(2000)], default="Information about user", null=True)

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nickname)
        super().save(*args, **kwargs)


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
        return f'{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
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
        return f'{self.user.nickname} - {self.post.title}'
