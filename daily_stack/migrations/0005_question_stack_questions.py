# Generated by Django 4.2.4 on 2023-09-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_stack', '0004_alter_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='none', max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='stack',
            name='questions',
            field=models.ManyToManyField(to='daily_stack.question'),
        ),
    ]
