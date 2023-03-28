# Generated by Django 4.1.7 on 2023-03-28 21:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_newsletter_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$', message='Incorrect expression of e-mail.')])),
                ('image', models.ImageField(null=True, upload_to='authors')),
            ],
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='caption',
            new_name='tag',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='users'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(30, django.core.validators.MaxLengthValidator(2000))])),
                ('post', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='Blog.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='Blog.user')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='Blog.author'),
        ),
    ]
