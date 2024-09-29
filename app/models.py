import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                              blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    # Contact Information
    address = models.TextField()

    # Additional Information
    profile_picture = models.ImageField(upload_to='media/patient_pic/', blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    date_of_registration = models.DateField(auto_now_add=True)
    account_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    last_visit_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    specialization = models.CharField(max_length=100)
    medical_license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    consultation_fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    working_hours = models.CharField(max_length=100)  # Example: "9 AM - 5 PM"
    days_available = models.CharField(max_length=100)  # Example: "Monday, Wednesday, Friday"
    clinic_address = models.TextField(null=True)
    education = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/doctor_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True)

    # Emergency Details
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)

    # Additional Fields
    consultation_type = models.CharField(max_length=20, choices=[('Online', 'Online'), ('Offline', 'Offline'), ('Both', 'Both')], default='Offline')
    appointment_slot_duration = models.PositiveIntegerField(default=30)  # duration in minutes
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)
    clinic_name = models.CharField(max_length=100, blank=True, null=True)
    is_available_for_emergency = models.BooleanField(default=False)
    max_daily_appointments = models.PositiveIntegerField(default=10)

    # Social Media
    linkedin_profile = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    date_of_registration = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Offline')


    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    symptoms = models.TextField()
    disease = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    appointment_type = models.CharField(max_length=20, choices=[('Online', 'Online'), ('In-person', 'In-person'), ('Telemedicine', 'Telemedicine')], default='In-person')
    priority = models.CharField(max_length=10, choices=[('Regular', 'Regular'), ('Emergency', 'Emergency')], default='Regular')
    follow_up_date = models.DateField(blank=True, null=True)
    appointment_status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled')
    doctor_notes = models.TextField(blank=True, null=True)
    consultation_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    is_confirmed = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    room_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    # def save(self, *args, **kwargs):
    #     # Ensure that the room_id is created automatically only if not set
    #     if self.appointment_type == 'Online' and not self.room_id:
    #         self.room_id = str(uuid.uuid4())  # Generate a unique UUID for the room_id
    #     super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.appointment_date}"
