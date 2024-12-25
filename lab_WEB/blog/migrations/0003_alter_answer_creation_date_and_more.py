# Generated by Django 4.1.7 on 2023-11-09 07:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_question_tags_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.CreateModel(
            name='QuestionLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.user')),
            ],
        ),
    ]
