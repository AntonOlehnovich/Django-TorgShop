# Generated by Django 3.2 on 2021-05-05 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0006_increase_name_max_length'),
        ('user', '0002_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.currency'),
        ),
    ]
