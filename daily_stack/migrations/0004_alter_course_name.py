# Generated by Django 4.2.4 on 2023-09-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_stack', '0003_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
