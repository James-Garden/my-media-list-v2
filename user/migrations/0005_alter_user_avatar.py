# Generated by Django 4.0.5 on 2022-06-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_deletion_date_user_marked_for_deletion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpg', upload_to='avatars'),
        ),
    ]