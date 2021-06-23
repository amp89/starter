# Generated by Django 3.2.4 on 2021-06-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration_timestamp', models.PositiveIntegerField(default=0)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]