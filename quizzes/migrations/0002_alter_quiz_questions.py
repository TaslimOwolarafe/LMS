# Generated by Django 4.1.2 on 2022-12-12 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(blank=True, null=True, to='quizzes.question'),
        ),
    ]