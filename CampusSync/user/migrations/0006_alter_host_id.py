# Generated by Django 5.0.3 on 2024-04-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_host_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
