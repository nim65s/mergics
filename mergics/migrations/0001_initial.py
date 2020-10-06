# Generated by Django 3.1.2 on 2020-10-06 10:04

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ndh.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ICSInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'url')},
            },
            bases=(ndh.models.Links, models.Model),
        ),
        migrations.CreateModel(
            name='ICSOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('inputs', models.ManyToManyField(to='mergics.ICSInput')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'slug')},
            },
            bases=(ndh.models.Links, models.Model),
        ),
    ]
