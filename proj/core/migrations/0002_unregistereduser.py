# Generated by Django 4.0.6 on 2022-07-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnregisteredUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('telegramId', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
