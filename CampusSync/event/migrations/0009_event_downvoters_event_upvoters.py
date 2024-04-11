# Generated by Django 5.0.3 on 2024-04-10 08:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_alter_comment_event'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='downvoters',
            field=models.ManyToManyField(related_name='downvote_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='upvoters',
            field=models.ManyToManyField(related_name='upvote_events', to=settings.AUTH_USER_MODEL),
        ),
    ]