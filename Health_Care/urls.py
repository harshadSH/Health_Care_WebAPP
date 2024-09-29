"""SIH_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/',login,name='login'),
    path('logout/', logout_view, name='logout'),
    path('d_sidebar/', d_sidebar, name='d_sidebar'),
    path('doctor_reg', doctor_reg, name='doctor_reg'),
    path('patient_reg', patient_reg, name='patient_reg'),
    path('patient_home', patient_home, name='patient_home'),
    path('doctor_home', doctor_home, name='doctor_home'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('book-appointment/<uuid:doctor_id>/', book_appointment, name='book_appointment'),
    path('appointment_history/', appointment_history, name='appointment_history'),
    path('chatbot/', chatbot, name='chatbot'),
    path('appointment-details/<uuid:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('scheduled-appointments/', scheduled_appointments, name='scheduled_appointments'),
    path('cancel-appointment/', cancel_appointment, name='cancel_appointment'),
    path('meeting/',videocall, name='meeting'),
    path('joinroom/<str:room_id>/', joinroom, name='joinroom'),
    path('appointment/start/<uuid:appointment_id>/', start_appointment, name='start_appointment'),
    path('doctor-appointments/', doctor_appointments, name='doctor_appointments'),
    path('profile/', doctor_profile, name='doctor_profile'),
    path('doctor/profile/edit/', edit_doctor_profile, name='edit_doctor_profile'),
    path('appointment/<uuid:appointment_id>/', d_appointment_detail, name='d_appointment_detail'),
    path('doctors/', doctor_list, name='doctor_list'),
    path('doctor/<uuid:doctor_id>/', doctor_detail, name='doctor_detail'),
    path('predict/', predict, name='predict'),
    path('diabetes_predict/', diabetes_predict, name='diabetes_predict'),
    #path('appointment/start/<uuid:appointment_id>/', start_appointment, name='start_appointment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
