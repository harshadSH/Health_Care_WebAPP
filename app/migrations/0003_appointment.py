# Generated by Django 3.2 on 2024-09-24 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_doctor_date_of_birth_doctor_date_of_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('symptoms', models.TextField()),
                ('disease', models.CharField(blank=True, max_length=100, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('prescription', models.TextField(blank=True, null=True)),
                ('prescription_file', models.FileField(blank=True, null=True, upload_to='prescriptions/')),
                ('appointment_type', models.CharField(choices=[('Online', 'Online'), ('In-person', 'In-person'), ('Telemedicine', 'Telemedicine')], default='In-person', max_length=20)),
                ('priority', models.CharField(choices=[('Regular', 'Regular'), ('Emergency', 'Emergency')], default='Regular', max_length=10)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('appointment_status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=20)),
                ('doctor_notes', models.TextField(blank=True, null=True)),
                ('consultation_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('cancellation_reason', models.TextField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
    ]
