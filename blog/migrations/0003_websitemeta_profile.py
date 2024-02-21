# Generated by Django 5.0.1 on 2024-02-08 09:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_slice_tag_slug_post_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('about', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='userImage')),
                ('bio', models.CharField(max_length=150, null=True)),
                ('slug', models.SlugField()),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profileUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
