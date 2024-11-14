# diabetes_predictor_app/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import pickle
import numpy as np
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from .forms import DiabetesForm
from .models import *

# Load the saved model
model_path = "diabetes_predictor_app/ml_models/diabetes_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Use auth_login to avoid conflict with view name
            if request.user.role=='patient':
                return redirect('/')
            else:
                
                return redirect('doctorpage')  # Redirect to the name of the URL mapped to the index view
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')  # Redirect to the login URL or view name
    else:
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)  # Use auth_logout to avoid conflict with view name
    return redirect('login')  # Redirect to the login page or any other URL


@login_required(login_url="login")
def assign_patient(request, patient_id):
    if request.method == "POST" and request.user.role == "doctor":
        patient = get_object_or_404(Patient, id=patient_id)
        doctor_profile = request.user.doctorprofile
        
        # Check if patient is already assigned
        if patient.doctor is not None:
            return JsonResponse({
                'status': 'error',
                'message': 'Patient is already assigned to a doctor'
            })
        
        # Assign patient to doctor
        patient.doctor = doctor_profile
        patient.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Patient successfully assigned'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })
@login_required(login_url="login")
def doctor_page(request):
    if request.user.role=="doctor":
         # Access the doctor's profile
        doctor_profile = request.user.doctorprofile
        
        # Get all patients assigned to this doctor
        patients = Patient.objects.filter(doctor=doctor_profile)
        unassigned_patients=Patient.objects.filter(doctor__isnull=True)
        total_number_of_patients=patients.count()
        context = {
            'patients': patients,
            'doctor':doctor_profile,
            'total_number_of_patients':total_number_of_patients,
            'unassigned_patients':unassigned_patients,
        }
        return render(request, 'doctor_home.html', context)  # Add .html to template name
    else:
        return HttpResponse("Access denied!")
        
      


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        patient=request.POST.get('patient')
        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('signup')
        elif User.objects.filter(email=email_address).exists():
            messages.info(request, "Email is already taken")
            return redirect('signup')
        else:
            # Create user and related profile based on role
            print(f"Username: {username}, Role: {role}, Email: {email_address}")
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                role=role,
                password=password,
                email=email_address,
                username=username
            )
            
            if role == 'doctor':
                newdoctor=DoctorProfile.objects.create(user=user, license_number=0)
                try:
                    assigning_doctor_to_patient=Patient.objects.get(id=patient)
                    assigning_doctor_to_patient.doctor=newdoctor
                except:
                    print("No Patient exists")
            elif role == 'patient':
                Patient.objects.create(user=user)
            
            return redirect('login')
    else:
        unassigned_patients=Patient.objects.filter(doctor__isnull=True)
        return render(request, 'signup.html', {'patients':unassigned_patients})

@login_required(login_url="login")
def predict_diabetes(request):
    if request.user.role=='patient':
        
        if request.method == 'POST':
            form = DiabetesForm(request.POST)
            name = request.POST.get('Name')
            
            if form.is_valid():
                # Extract and prepare data from form
                data = [
                    form.cleaned_data['Pregnancies'],
                    form.cleaned_data['Glucose'],
                    form.cleaned_data['BloodPressure'],
                    form.cleaned_data['SkinThickness'],
                    form.cleaned_data['Insulin'],
                    form.cleaned_data['BMI'],
                    form.cleaned_data['DiabetesPedigreeFunction'],
                    form.cleaned_data['Age']
                ]

                # Predict probability and class
                prediction_proba = model.predict_proba([data])[0][1] * 100  # Probability for diabetic class
                if prediction_proba < 40:
                    result = "Likely not Diabetic"
                elif 40 <= prediction_proba <= 70:
                    result = "Borderline"
                else:
                    result = "Likely Diabetic"

                # Save prediction to Patient model
                Patient.objects.create(
                    Name=name,
                    Pregnancies=data[0],
                    Glucose=data[1],
                    BloodPressure=data[2],
                    SkinThickness=data[3],
                    Insulin=data[4],
                    BMI=data[5],
                    DiabetesPedigreeFunction=data[6],
                    Age=data[7],
                    Result=result,
                    Prediction=round(prediction_proba, 2)
                )

                return render(request, 'result.html', {
                    'result': result,
                    'probability': round(prediction_proba, 2)
                })

        else:
            form = DiabetesForm()

        return render(request, 'index.html', {'form': form})
    else:
        return redirect("wronguser")
def wronguser(request):
    return render(request, 'wrong_user.html')