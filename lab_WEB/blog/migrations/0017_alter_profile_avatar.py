# Generated by Django 4.1.7 on 2023-12-17 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_answerreaction_questionreaction_alter_tag_word_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='anon.jpg', null=True, upload_to='avatar/%Y/%m/%d'),
        ),
    ]
