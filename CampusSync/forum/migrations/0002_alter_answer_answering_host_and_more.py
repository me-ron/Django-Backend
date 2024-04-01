# Generated by Django 5.0.3 on 2024-04-01 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        ('user', '0002_alter_host_account_pic_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answering_host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answering_host', to='user.host'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answering_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answering_user', to='user.user'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_of_answer', to='forum.question'),
        ),
        migrations.AlterField(
            model_name='forum',
            name='questions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_questions', to='forum.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_question_asker', to='user.user'),
        ),
    ]