# Generated by Django 3.2.16 on 2022-12-15 19:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Введите корректный код цвета.', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')], verbose_name='Цветовой код тэга'),
        ),
    ]