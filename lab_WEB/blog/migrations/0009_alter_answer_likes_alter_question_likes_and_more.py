# Generated by Django 4.1.7 on 2023-11-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_answer_likes_alter_question_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='answer_liked_by', to='blog.user'),
        ),
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='liked_by', to='blog.user'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='blog.tag'),
        ),
    ]
