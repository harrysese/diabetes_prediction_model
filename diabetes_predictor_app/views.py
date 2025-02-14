from django.utils import timezone
from datetime import timedelta
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import pickle
import numpy as np
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from .forms import DiabetesForm
from django.core.mail import send_mail
from .models import *
from diabetes_predictor_app.email import send_remark_email
from typing import List, Union
from django.db.models import Min, Max, Avg
from django.core.exceptions import ValidationError

# Load the saved model
model_path = "diabetes_predictor_app/ml_models/diabetes_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

def index(request):
    return render(request, 'index.html')


def patient_detail(request: HttpRequest, patient_id: int):
    user = get_object_or_404(User, id=patient_id)
    patients = Patient.objects.filter(user=user).order_by('-created_at')
    print(patients)
    # Prepare chart data
    chart_data = {
        'labels': [p.created_at.strftime("%Y-%m-%d") for p in patients],
        'glucose': [p.Glucose for p in patients],
        'bmi': [float(p.BMI) for p in patients],
        'results': [p.Result for p in patients]
    }
    
    context = {
        'user': user,
        'patients': patients,
        'chart_data': chart_data,
    }
    return render(request, 'patient_detail.html', context)
    


def login(request:HttpRequest):
    """"
    Args:
    request(obj)
    Grabs the inputted username and password from the POST HttpRequest
    and queries the database for a match.
    If there is it calls the login method which creates a session for the user and redirects them
    to their respective pages depending on their role
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Use auth_login to avoid conflict with view name
            if request.user.role=='patient':
                print("USer is a patient")
                return redirect('patient_dashboard')
            else:
                
                return redirect('doctor')  # Redirect to the name of the URL mapped to the index view
        else:
            messages.info(request, 'Incorrect username or password')
            return redirect('login')  # Redirect to the login URL or view name
    else:
        return render(request, 'login.html')


def logout(request:HttpRequest):
    auth_logout(request)  # Use auth_logout to avoid conflict with view name
    return redirect('index')  # Redirect to the login page or any other URL


def submitremark(request, patient_id):
    if request.method=="POST" and request.user.role=='doctor':
        data = json.loads(request.body)
        remark = data.get('remark', '')  #
        patient=get_object_or_404(Patient, id=patient_id)
        patient.remark=remark
        patient.save()
        if patient.user.email:
            try:
                
               send_remark_email(
            patient=patient,
            doctor_name=request.user.doctorprofile,
            remark=remark,
            email=patient.user.email
        )
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
        return JsonResponse({
            'status':'success',
            'message':'Remark assigned to patient',
        })
    else:
        return JsonResponse(
            {
            'status':'error',
                'message':'Invalid method!',
        }, status=400)
        

def patient(request):
    if request.user.role=='patient':
        patient = Patient.objects.filter(user=request.user).order_by('created_at')

        if patient.exists():
            latest_test = patient.last()
        else:
            latest_test = None

        test_dates = [test.created_at.strftime("%Y-%m-%d") for test in patient if test.created_at]
        glucose_data = [float(test.Glucose) for test in patient if test.Glucose is not None]
        bmi_data = [float(test.BMI) for test in patient if test.BMI is not None]

        avg_glucose = sum(glucose_data) / len(glucose_data) if glucose_data else 0
        bmi_percent = min(100, (latest_test.BMI / 30) * 100) if latest_test and latest_test.BMI else 0
        glucose_percent = min(100, (latest_test.Glucose / 200) * 100) if latest_test and latest_test.Glucose else 0
        age_percent = min(100, (latest_test.Age / 80) * 100) if latest_test and latest_test.Age else 0

        context = {
            'tests': patient,
            'latest_test': latest_test if latest_test else {},
            'test_dates': json.dumps(test_dates),
            'glucose_data': json.dumps(glucose_data),
            'bmi_data': json.dumps(bmi_data),
            'avg_glucose': avg_glucose,
            'next_checkup': timezone.now() + timedelta(days=30),
            'bmi_percent': bmi_percent,
            'glucose_percent': glucose_percent,
            'age_percent': age_percent,
        }
        return render(request, 'patient_dashboard.html', context)
    else:
        messages.info(request, 'You need to login as a patient')
        return redirect('wronguser')
        
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
    if request.user.role != "doctor":
        messages.error(request, "You need to log in as a Doctor")
        return redirect("wronguser")

    try:
        # Access the doctor's profile
        doctor_profile = request.user.doctorprofile

        # Get all patients assigned to this doctor (distinct by user)
        patient_ids = (
            Patient.objects.filter(doctor=doctor_profile)
            .values('user')  # Group by user
            .annotate(id=Max('id'))  # Keep the Latest patient record for each user
            .values_list('id', flat=True)  # Extract the IDs of distinct patients
        )

        # Fetch the full patient objects for the distinct IDs
        patients = Patient.objects.filter(id__in=patient_ids).select_related('user')
        #Get High Risk Patients by checking if their prediction is greater than 70%
        high_risk_patients=Patient.objects.filter(Prediction__gt=70, id__in=patient_ids).select_related('user')
        # Add initials to each patient dynamically
        for patient in patients:
            patient.initials = f"{patient.user.first_name[0].upper()}{patient.user.last_name[0].upper()}"

        # Get unassigned patients (patients without a doctor)
        unassigned_patients = Patient.objects.filter(doctor__isnull=True).select_related('user')

        # Calculate total number of patients assigned to the doctor
        total_number_of_patients = patients.count()
        doctor_initials=f'{request.user.first_name[0]}{request.user.last_name[0]}'
        print(doctor_initials)
        # Prepare context for rendering
        context = {
            'patients': patients,
            'doctor': doctor_profile,
            'total_number_of_patients': total_number_of_patients,
            'unassigned_patients': unassigned_patients,
            'high_risk_patients':high_risk_patients.count(),
            'doctor_initials':doctor_initials,
        }

        return render(request, 'doctor_home.html', context)

    except AttributeError:
        # Handle cases where `request.user.doctorprofile` does not exist
        messages.error(request, "Doctor profile not found. Please contact support.")
        return redirect('wronguser')
      


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('signup')
        elif User.objects.filter(email=email_address).exists():
            messages.info(request, "Email is already taken")
            return redirect('signup')
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                role=role,
                password=password,
                email=email_address,
                username=username
            )
            
            if role == 'doctor':
                DoctorProfile.objects.create(user=user, license_number=0)
           
            elif role == 'patient':
                Patient.objects.create(user=user)
            
            return redirect('login')
    else:
        unassigned_patients=Patient.objects.filter(doctor__isnull=True)
        return render(request, 'signup.html', {'patients':unassigned_patients})

@login_required(login_url="login")

def predict_diabetes(request):
    if request.user.role == 'patient':
        if request.method == 'POST':
            form = DiabetesForm(request.POST)
            doctor = Patient.objects.filter(user=request.user).first()
            print(doctor)
            name=Patient.objects.filter(user=request.user).first()
            if form.is_valid():
                print("Form is valid. Cleaned data:", form.cleaned_data)
                # Extract and prepare data from form
                # name = form.cleaned_data.get('Name', 'Unknown')
                try:
                    data = [
                            int(form.cleaned_data['Pregnancies']),
                            float(form.cleaned_data['Glucose']),
                            float(form.cleaned_data['BloodPressure']),
                            float(form.cleaned_data['SkinThickness']),
                            float(form.cleaned_data['Insulin']),
                            float(form.cleaned_data['BMI']),
                            float(form.cleaned_data['DiabetesPedigreeFunction']),
                            int(form.cleaned_data['Age'])
                                                    ]
                    print("Extracted data:", data)
                except:
                    print("Error while extracting data", str(e))
                    return render(request, 'prediction_form.html',{'form':form})
                # Predict probability and classify
                prediction_proba = model.predict_proba([data])[0][1] * 100# Probability for diabetic class
                prediction_proba = max(0, min(100, prediction_proba))# Clamp probability
                print("Prediction probability:", prediction_proba)
                LOW_RISK_THRESHOLD = 40
                HIGH_RISK_THRESHOLD = 70

                if prediction_proba < LOW_RISK_THRESHOLD:
                    result = "Likely not Diabetic"
                elif LOW_RISK_THRESHOLD <= prediction_proba <= HIGH_RISK_THRESHOLD:
                    result = "Borderline"
                else:
                    result = "Likely Diabetic"
                print("Prediction result:", result)
                try:
                    # Create and validate patient record
                    Patient.objects.create(
                        user=request.user,
                        Name=name.user.first_name,
                        Pregnancies=data[0],
                        Glucose=data[1],
                        BloodPressure=data[2],
                        SkinThickness=data[3],
                        Insulin=data[4],
                        BMI=data[5],
                        DiabetesPedigreeFunction=data[6],
                        Age=data[7],
                        Result=result,
                        Prediction=float(round(prediction_proba, 2)),
                        doctor=doctor.doctor
                    )
                    print("Patient object data:", vars(patient))
                   
                    print("Rendering result page with result:", result, "and probability:", prediction_proba)

                    messages.success(request, "Test result saved successfully!")
                except ValidationError as e:
                    messages.error(request, f"Invalid data: {e}")
                    print('Invalid data')
                    return render(request, 'prediction_form.html', {'form': form})
                except Exception as e:
                    messages.error(request, f"Failed to save test result: {str(e)}")
                    print('failed to save test result')
                    return redirect("patient_dashboard")

                return redirect('patient_result')
            else:
                messages.error(request, "Form contains errors. Please check your input.")
                print('form contains errors')
                return render(request, 'prediction_form.html', {'form': form})

        else:
            form = DiabetesForm()
            return render(request, 'prediction_form.html', {
                'form': form,
                'role': request.user.role
            })
    else:
        messages.error(request, "You need to log in as a patient")
        return redirect("wronguser")

def result(request:HttpRequest):
    patient=Patient.objects.filter(user=request.user).latest('created_at')
    context={
        'result':patient.Result,
        'probability':patient.Prediction
    }
    return render(request, 'result.html', context=context)

def wronguser(request):
    return render(request, 'wrong_user.html')