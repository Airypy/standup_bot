# Generated by Django 3.1 on 2020-08-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('today', models.CharField(max_length=400)),
                ('yesterday', models.CharField(max_length=400)),
                ('obstacles', models.CharField(max_length=400)),
            ],
        ),
    ]
