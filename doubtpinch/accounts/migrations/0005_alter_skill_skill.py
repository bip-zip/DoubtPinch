# Generated by Django 3.2.5 on 2021-09-22 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_skill_userskill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]