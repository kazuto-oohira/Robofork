# Generated by Django 2.0 on 2018-03-20 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robofork_app', '0005_auto_20180318_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='robofork_app.Location'),
        ),
    ]
