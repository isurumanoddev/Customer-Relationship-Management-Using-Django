# Generated by Django 4.1.7 on 2023-03-15 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
