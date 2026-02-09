from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Appointment, Patient

def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'myapp/home.html', {'doctors': doctors})


def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        date = request.POST['date']
        time = request.POST['time']

        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(user=request.user)

        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date=date,
            time=time
        )
        return redirect('home')

    doctors = Doctor.objects.all()
    return render(request, 'myapp/book.html', {'doctors': doctors})


def register(request):
    if request.method == 'POST':
        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        if role == 'doctor':
            specialization = request.POST['specialization']
            Doctor.objects.create(
                user=user,
                phone=phone,
                specialization=specialization
            )
        else:
            age = request.POST['age']
            gender = request.POST['gender']
            address = request.POST['address']
            Patient.objects.create(
                user=user,
                phone=phone,
                age=age,
                gender=gender,
                address=address
            )

        return redirect('login')

    return render(request, 'myapp/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'myapp/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    if hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        return render(request, 'myapp/doctor_dashboard.html', {'appointments': appointments})

    elif hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
        return render(request, 'myapp/patient_dashboard.html', {'appointments': appointments})

    return redirect('login')

