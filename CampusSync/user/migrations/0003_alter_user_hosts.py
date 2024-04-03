# Generated by Django 5.0.3 on 2024-04-03 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_hosts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hosts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_hosts', to='user.host'),
        ),
    ]