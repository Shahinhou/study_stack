# Generated by Django 4.2.4 on 2023-08-30 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_stack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('difficulty', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('name', models.CharField(default='essay', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='stack',
            name='assignments',
            field=models.ManyToManyField(to='daily_stack.assignment'),
        ),
    ]
