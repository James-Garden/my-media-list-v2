# Generated by Django 4.0.5 on 2022-06-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_avatar_url_profile_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('P', 'Not Specified'), ('M', 'Male'), ('F', 'Female'), ('N', 'Non-Binary')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date_privacy',
            field=models.CharField(choices=[('PR', 'Private'), ('PA', 'Public'), ('PY', 'Public (Year Only)'), ('PM', 'Public (Year and Month Only)')], default='PR', max_length=2),
        ),
    ]