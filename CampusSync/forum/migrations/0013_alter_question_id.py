# Generated by Django 5.0.3 on 2024-04-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_remove_question_author_id_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
