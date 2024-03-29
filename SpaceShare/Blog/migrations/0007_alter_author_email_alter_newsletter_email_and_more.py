# Generated by Django 4.1.7 on 2023-04-25 13:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_alter_newsletter_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator('^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f!#-[]-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f!-ZS-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])+)\\])$', message='Incorrect expression of e-mail.')]),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f!#-[]-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f!-ZS-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])+)\\])$', message='Incorrect expression of e-mail.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f!#-[]-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f!-ZS-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])+)\\])$', message='Incorrect expression of e-mail.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='users/default.jpg', null=True, upload_to='users'),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^(?=.*?[a-zA-Z\\d])[a-zA-Z][a-zA-Z\\d_-]{2,28}[a-zA-Z\\d]$', message='Login must be between 4 and 30 characters long and must start with a letter and end with a letter or number. It can contain a floor and dash between the start and end.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[.~!@#$%^&*()+=[\\]\\;:\'"/,|{}<>?])[a-zA-Z0-9.~!@#$%^&*()+=[\\]\\;:\'"/,|{}<>?]{8,40}$', message='Password must be between 8 and 40 characters long, contain one lowercase and one uppercase letter, one number and one special character.')]),
        ),
    ]
