# Generated by Django 4.0.4 on 2022-08-30 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='communication',
            field=models.CharField(default='', max_length=256, verbose_name='Способ связи'),
        ),
    ]
