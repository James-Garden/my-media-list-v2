# Generated by Django 4.0.5 on 2022-06-14 00:19

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'That username is taken.'}, help_text='Required. 2 to 20 characters. Must start with a capital letter, and only contain letters, digits and _', max_length=20, unique=True, validators=[utils.validators.validate_username], verbose_name='username'),
        ),
    ]
