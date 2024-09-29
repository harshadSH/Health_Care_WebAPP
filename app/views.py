from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

def index(request):
    return render(request, 'index.html')

def d_sidebar(request):
    return render(request, 'd_sidebar.html')

def patient_reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')
        gender = request.POST.get('gender')

        # Check if passwords match
        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'patient_reg.html', {'error_message': error_message})

        # Check if the email is already in use
        if User.objects.filter(username=email).exists():
            error_message = "Email is already in use."
            return render(request, 'patient_reg.html', {'error_message': error_message})

        # Create the user and patient
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        patient = Patient.objects.create(user=user,date_of_birth=date_of_birth, phone_number=phone_number, profile_picture=profile_picture, gender=gender)

        # Redirect to login or another page
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')  # Assuming there's a login page

    return render(request, 'patient_reg.html')


def doctor_reg(request):
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        specialization = request.POST.get('specialization')
        years_of_experience = request.POST.get('years_of_experience')
        education = request.POST.get('education')
        medical_license_number = request.POST.get('medical_license_number')
        clinic_address = request.POST.get('clinic_address')
        working_hours = request.POST.get('working_hours')
        days_available = request.POST.get('days_available')
        consultation_mode = request.POST.get('consultation_mode')
        profile_picture = request.FILES.get('profile_picture')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'doctor_reg.html')

        # Check if the medical license number is unique
        if Doctor.objects.filter(medical_license_number=medical_license_number).exists():
            messages.error(request, "Medical License Number is already in use.")
            return render(request, 'doctor_reg.html')

        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'doctor_reg.html', {'error_message': error_message})

        try:
            # Create a new user for the doctor
            user = User.objects.create_user(
                username=email, email=email, first_name=first_name, last_name=last_name, password=password
            )

            # Create the Doctor instance
            doctor = Doctor.objects.create(
                user=user,
                phone_number=phone_number,
                specialization=specialization,
                years_of_experience=years_of_experience,
                education=education,
                medical_license_number=medical_license_number,
                clinic_address=clinic_address,
                working_hours=working_hours,
                days_available=days_available,
                consultation_type=consultation_mode,
                profile_picture=profile_picture
            )

            messages.success(request, "Doctor registered successfully!")
            return redirect('login')  # Redirect after registration

        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'doctor_reg.html')

    return render(request, 'doctor_reg.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            # Redirect based on user type
            if hasattr(user, 'patient'):
                return redirect('patient_home')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_home')
            else:
                messages.error(request, "Invalid user type.")
                return redirect('login')
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


from django.contrib.auth import logout
def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('index')

@login_required
def patient_home(request):
    return render(request, 'patient_home.html')


@login_required
def book_appointment(request, doctor_id=None):
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        symptoms = request.POST.get('symptoms')
        details = request.POST.get('details')
        appointment_type = request.POST.get('appointment_type')
        priority = request.POST.get('priority')
        doctor_id = request.POST.get('doctor')

        # Get the patient instance based on the logged-in user
        patient_instance = Patient.objects.get(user=request.user)

        # Fetch the doctor based on the selected doctor ID
        selected_doctor = get_object_or_404(Doctor, id=doctor_id)

        # Validate the appointment date (optional but recommended)
        if timezone.now() > timezone.make_aware(timezone.datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M')):
            return render(request, 'book_appointment.html', {
                'doctors': Doctor.objects.all(),
                'error': 'Appointment date cannot be in the past.',
                'selected_doctor': selected_doctor
            })

        # Save the appointment
        appointment = Appointment.objects.create(
            appointment_date=appointment_date,
            symptoms=symptoms,
            details=details,
            appointment_type=appointment_type,
            priority=priority,
            doctor=selected_doctor,
            patient=patient_instance,
        )

        # Send confirmation email (uncomment if email functionality is set up)
        # send_mail(
        #     'Appointment Confirmation',
        #     f'Your appointment has been booked for {appointment.appointment_date}.',
        #     'from@example.com',
        #     [request.user.email],
        #     fail_silently=False,
        # )

        return redirect('appointment_history')  # Redirect to an appointment history page after booking

    # Get all doctors to display in the dropdown list
    doctors = Doctor.objects.all()

    # Fetch the pre-selected doctor if provided (from URL or link)
    selected_doctor = None
    if doctor_id:
        selected_doctor = get_object_or_404(Doctor, id=doctor_id)

    return render(request, 'book_appointment.html', {
        'doctors': doctors,
        'selected_doctor': selected_doctor
    })

@login_required
def appointment_history(request):
    # Check if the logged-in user is a patient
    try:
        if hasattr(request.user, 'patient'):
            # Get the Patient instance related to the logged-in user
            patient = Patient.objects.get(user=request.user)
            # Fetch appointments related to this patient
            appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
            context = {'appointments': appointments, 'role': 'patient'}

        # Check if the logged-in user is a doctor
        elif hasattr(request.user, 'doctor'):
            # Get the Doctor instance related to the logged-in user
            doctor = Doctor.objects.get(user=request.user)
            # Fetch appointments related to this doctor
            appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
            context = {'appointments': appointments, 'role': 'doctor'}

        else:
            return render(request, 'error_page.html', {'message': 'User role not found.'})

        # Render the appointment history page with the fetched appointments
        return render(request, 'appointment_history.html', context)

    except (Patient.DoesNotExist, Doctor.DoesNotExist):
        return render(request, 'error_page.html', {'message': 'Record not found.'})

@login_required
def chatbot(request):
    return render(request, 'coming_soon.html', {'feature': 'Chat with AI Assistant'})

@login_required
def appointment_detail(request, appointment_id):
    # Get the appointment instance by ID
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Pass the appointment details to the template
    context = {
        'appointment': appointment
    }

    return render(request, 'appointment_detail.html', context)

@login_required
def get_appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    data = {
        'doctor': f"{appointment.doctor.user.first_name} {appointment.doctor.user.last_name}",
        'appointment_datetime': appointment.appointment_date.strftime("%Y-%m-%d %H:%M"),
        'symptoms': appointment.symptoms,
        'details': appointment.details,
        'disease': appointment.disease,
        'appointment_type': appointment.appointment_type,
        'prescription': appointment.prescription,
    }
    return JsonResponse(data)

@login_required
def scheduled_appointments(request):
    # Assuming the user is authenticated, and appointments are linked to a patient
    patient = request.user.patient  # Adjust this based on your authentication and user setup
    # Filter appointments with status 'Scheduled'
    appointments = Appointment.objects.filter(patient=patient, appointment_status='Scheduled')

    return render(request, 'scheduled_appointments.html', {'appointments': appointments})
@login_required
def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        cancellation_reason = request.POST.get('cancellation_reason')

        # Fetch the appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Update the status and add the cancellation reason
        appointment.appointment_status = 'Cancelled'
        appointment.cancellation_reason = cancellation_reason
        appointment.save()

        # Optional: Add a success message
        messages.success(request, 'Appointment has been successfully cancelled.')

        return redirect('scheduled_appointments')



@login_required
def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

def joinroom(request, room_id):
    # Fetch the appointment where room_id is initially null
    appointment = get_object_or_404(Appointment, room_id=room_id)

    # If room_id is null, generate a new unique room_id
    if not appointment.room_id:
        appointment.room_id = str(uuid.uuid4())  # Generate a unique UUID room ID
        appointment.save()

    # Redirect to the meeting page with the generated or existing room ID
    return redirect('/meeting?roomID=' + appointment.room_id)

def doctor_list(request):
    # Get all doctors initially
    doctors = Doctor.objects.all()

    # Handle search and filtering
    search_query = request.GET.get('search', '')
    specialization_filter = request.GET.get('specialization', '')

    if search_query:
        doctors = doctors.filter(name__icontains=search_query)

    if specialization_filter:
        doctors = doctors.filter(specialization__icontains=specialization_filter)

    # Pass doctors to the template
    context = {
        'doctors': doctors,
        'search_query': search_query,
        'specialization_filter': specialization_filter,
    }

    return render(request, 'doctor_list.html', context)

def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    context = {'doctor': doctor}
    return render(request, 'doctor_detail.html', context)

#------------------------------------------------------------------------------------------------
from django.http import HttpResponseForbidden

def start_appointment(request, appointment_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to start an appointment.")

    # Ensure the user is a doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseForbidden("Only doctors can start appointments.")

    # Fetch the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the appointment doctor matches the logged-in doctor
    if appointment.doctor != doctor:
        return HttpResponseForbidden("You are not the assigned doctor for this appointment.")

    # Generate the room ID if not already generated
    if not appointment.room_id:
        appointment.room_id = str(uuid.uuid4())  # Generate unique room ID
        appointment.save()

    # Redirect to the appointment detail page
    return redirect('d_appointment_detail', appointment_id=appointment.id)

def doctor_home(request):
    # Assuming the doctor is logged in
    doctor = request.user.doctor
    # Fetch doctor's upcoming appointments
    appointments = Appointment.objects.filter(doctor=doctor, appointment_status="Scheduled").order_by(
        'appointment_date')

    context = {
        'doctor': doctor,
        'appointments': appointments,
    }
    return render(request, 'doctor_home.html', context)


@login_required
def doctor_appointments(request):
    doctor = request.user.doctor  # Fetch the logged-in doctor
    today = timezone.now().date()

    # Filter based on query params
    filter_param = request.GET.get('filter')
    filter_date = request.GET.get('filter_date')

    if filter_param == 'today':
        appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date=today,
                                                  appointment_status="Scheduled")
    elif filter_param == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date=tomorrow,
                                                  appointment_status="Scheduled")
    elif filter_date:
        # Custom date filtering
        appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date=filter_date,
                                                  appointment_status="Scheduled")
    else:
        # Default to showing all scheduled appointments
        appointments = Appointment.objects.filter(doctor=doctor, appointment_status="Scheduled").order_by(
            'appointment_date')

    context = {
        'appointments': appointments,
    }
    return render(request, 'doctor_appointments.html', context)


@login_required
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        doctor.phone_number = request.POST.get('phone_number')
        doctor.specialization = request.POST.get('specialization')
        doctor.years_of_experience = request.POST.get('years_of_experience')
        doctor.consultation_fees = request.POST.get('consultation_fees')
        doctor.working_hours = request.POST.get('working_hours')
        doctor.days_available = request.POST.get('days_available')
        doctor.clinic_address = request.POST.get('clinic_address')
        doctor.education = request.POST.get('education')
        doctor.bio = request.POST.get('bio')
        doctor.date_of_birth = request.POST.get('date_of_birth')
        doctor.emergency_contact_name = request.POST.get('emergency_contact_name')
        doctor.emergency_contact_phone = request.POST.get('emergency_contact_phone')
        doctor.online_consultation = request.POST.get('online_consultation') == 'True'
        doctor.appointment_slot_duration = request.POST.get('appointment_slot_duration')
        doctor.languages_spoken = request.POST.get('languages_spoken')
        doctor.clinic_name = request.POST.get('clinic_name')
        doctor.is_available_for_emergency = request.POST.get('is_available_for_emergency') == 'True'
        doctor.linkedin_profile = request.POST.get('linkedin_profile')
        doctor.website = request.POST.get('website')
        doctor.status = request.POST.get('status')

        if 'profile_picture' in request.FILES:
            doctor.profile_picture = request.FILES['profile_picture']

        doctor.save()
        return redirect('doctor_profile')  # Redirect after saving to avoid re-posting on refresh

    return render(request, 'doctor_profile.html', {'doctor': doctor})


from .forms import DoctorProfileForm


def edit_doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        # Get the data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        specialization = request.POST.get('specialization')
        medical_license_number = request.POST.get('medical_license_number')
        years_of_experience = request.POST.get('years_of_experience')
        consultation_fees = request.POST.get('consultation_fees')
        working_hours = request.POST.get('working_hours')
        days_available = request.POST.get('days_available')
        clinic_address = request.POST.get('clinic_address')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_phone = request.POST.get('emergency_contact_phone')
        consultation_type = request.POST.get('consultation_mode')
        appointment_slot_duration = request.POST.get('appointment_slot_duration')
        languages_spoken = request.POST.get('languages_spoken')
        clinic_name = request.POST.get('clinic_name')
        is_available_for_emergency = request.POST.get('is_available_for_emergency') == 'on'
        max_daily_appointments = request.POST.get('max_daily_appointments')
        linkedin_profile = request.POST.get('linkedin_profile')
        website = request.POST.get('website')

        # Validate and update the doctor instance
        doctor.user.first_name = first_name
        doctor.user.last_name = last_name
        doctor.phone_number = phone_number

        # Convert date_of_birth to a proper date format
        if date_of_birth:
            try:
                doctor.date_of_birth = timezone.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                # Handle the error case as needed, e.g., set to None or display a message
                doctor.date_of_birth = None

        doctor.specialization = specialization
        doctor.medical_license_number = medical_license_number
        doctor.years_of_experience = years_of_experience
        doctor.consultation_fees = consultation_fees
        doctor.working_hours = working_hours
        doctor.days_available = days_available
        doctor.clinic_address = clinic_address
        doctor.emergency_contact_name = emergency_contact_name
        doctor.emergency_contact_phone = emergency_contact_phone
        doctor.consultation_type = consultation_type
        doctor.appointment_slot_duration = appointment_slot_duration
        doctor.languages_spoken = languages_spoken
        doctor.clinic_name = clinic_name
        doctor.is_available_for_emergency = is_available_for_emergency
        doctor.max_daily_appointments = max_daily_appointments
        doctor.linkedin_profile = linkedin_profile
        doctor.website = website

        # Save changes
        doctor.user.save()
        doctor.save()

        return redirect('doctor_profile')

    return render(request, 'edit_doctor_profile.html', {'doctor': doctor})


def d_appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # If the doctor is updating the appointment details
        appointment.prescription = request.POST.get('prescription', appointment.prescription)
        appointment.disease = request.POST.get('disease', appointment.disease)
        appointment.consultation_fees = request.POST.get('consultation_fees', appointment.consultation_fees)
        appointment.note = request.POST.get('note', appointment.note)
        appointment.doctor_notes = request.POST.get('doctor_notes', appointment.doctor_notes)

        # Save the appointment details
        appointment.save()

        return redirect('d_appointment_detail', appointment_id=appointment.id)

    return render(request, 'd_appointment_detail.html', {'appointment': appointment})


# def start_appointment(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)
#
#     if appointment.appointment_type == 'Online' and appointment.is_confirmed:
#         send_email_notification(appointment.patient.user.email, appointment)
#
#     return redirect('d_appointment_detail', appointment_id=appointment.id)


# def send_email_notification(email, appointment):
#     subject = 'Your Appointment has Started'
#     message = f"Your appointment with Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name} has started."
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

from django.shortcuts import render
from django.http import JsonResponse
import joblib
import numpy as np

# Load the model
model = joblib.load('D:/SIH_Project/app/voting_classifier_model.pkl')

def predict(request):
    if request.method == 'POST':
        # Retrieve the data from the POST request individually
        mean_radius = request.POST.get('mean_radius')
        mean_texture = request.POST.get('mean_texture')
        mean_perimeter = request.POST.get('mean_perimeter')
        mean_area = request.POST.get('mean_area')
        mean_compactness = request.POST.get('mean_compactness')
        mean_concavity = request.POST.get('mean_concavity')
        worst_radius = request.POST.get('worst_radius')
        worst_perimeter = request.POST.get('worst_perimeter')
        worst_area = request.POST.get('worst_area')
        worst_concavity = request.POST.get('worst_concavity')

        # Convert the data to float and prepare it for model input
        input_data = np.asarray([
            float(mean_radius), float(mean_texture), float(mean_perimeter), float(mean_area),
            float(mean_compactness), float(mean_concavity), float(worst_radius),
            float(worst_perimeter), float(worst_area), float(worst_concavity)
        ]).reshape(1, -1)

        # Make the prediction
        prediction = model.predict(input_data)

        # Interpret the prediction result
        result = 'Malignant' if prediction[0] == 0 else 'Benign'

        # Return the prediction as a JSON response
        return JsonResponse({'prediction': result})

    # Render the HTML template for the form
    return render(request, 'predict.html')


model1 = joblib.load('D:/SIH_Project/dt.pkl')  # Replace with your model file
scaler = joblib.load('D:/SIH_Project/scaler.pkl')  # Replace with your scaler file

def diabetes_predict(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        pregnancies = float(request.POST.get('pregnancies'))
        glucose = float(request.POST.get('glucose'))
        blood_pressure = float(request.POST.get('blood_pressure'))
        skin_thickness = float(request.POST.get('skin_thickness'))
        insulin = float(request.POST.get('insulin'))
        bmi = float(request.POST.get('bmi'))
        dpf = float(request.POST.get('dpf'))
        age = float(request.POST.get('age'))

        # Convert form data to a NumPy array
        input_data = np.asarray([pregnancies, glucose, blood_pressure, skin_thickness,
                                 insulin, bmi, dpf, age]).reshape(1, -1)

        # Standardize input data
        std_data = scaler.transform(input_data)

        # Make a prediction using the model
        prediction = model1.predict(std_data)

        # Generate health advice based on the prediction
        advice = provide_health_advice(input_data, prediction)

        # Interpret prediction result
        result = 'The person is not diabetic' if prediction[0] == 0 else 'The person is diabetic'

        # Return both prediction and advice as a JSON response
        return JsonResponse({'prediction': result, 'advice': advice})

    # If it's a GET request, render the HTML page
    return render(request, 'diabetes_predict.html')

def provide_health_advice(input_data, prediction):
    advice = ""
    if prediction[0] == 0:
        advice = "The person is not diabetic.\n"
        pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age = input_data[0]

        if glucose > 140:
            advice += "However, your glucose level is higher than normal. Consider a low sugar diet and regular exercise.\n"
        if blood_pressure > 80:
            advice += "Your blood pressure is higher than normal. Try to reduce salt intake and consult your doctor.\n"
        if insulin > 200:
            advice += "Your insulin levels are higher than normal. This might indicate insulin resistance. Consult a healthcare professional.\n"
        if bmi > 25:
            advice += "Your BMI indicates that you are overweight. Regular exercise and a balanced diet can help maintain a healthy weight.\n"
        if age > 45:
            advice += "Since you're above 45, it's important to regularly monitor your blood sugar levels to prevent diabetes.\n"
    else:
        advice = "The person is diabetic.\n"
        advice += "- Follow a diabetes-friendly diet rich in whole grains, vegetables, and lean proteins.\n"
        advice += "- Engage in regular physical activity to help control blood sugar levels.\n"
        advice += "- Monitor your blood sugar levels regularly and follow your doctor's advice on medications.\n"
        advice += "- Maintain a healthy weight and manage stress through relaxation techniques.\n"

    return advice