# Generated by Django 4.2.5 on 2023-09-19 08:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_menu', '0005_alter_product_guid_alter_product_max_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_tax',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='guid',
            field=models.CharField(default=uuid.UUID('765792cf-936a-4267-a728-528e32938ae0'), max_length=100, unique=True),
        ),
    ]
