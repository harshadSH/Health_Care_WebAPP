# Generated by Django 3.2 on 2024-09-26 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_doctor_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/doctor_pics/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/patient_pic/'),
        ),
    ]
