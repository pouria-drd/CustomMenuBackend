# Generated by Django 4.2.5 on 2023-11-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customerlogincode_failed_tries'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerlogincode',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]