# Generated by Django 3.1.2 on 2021-07-06 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dpapp', '0005_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_answer', to='dpapp.answer'),
        ),
    ]
