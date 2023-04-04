# Generated by Django 4.1.7 on 2023-04-03 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(default='Author Info', validators=[
                                   django.core.validators.MinLengthValidator(30, django.core.validators.MaxLengthValidator(2000))]),
        ),
    ]