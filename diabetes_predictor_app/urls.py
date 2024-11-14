from .views import *
from django.urls import path

urlpatterns=[
    path('', predict_diabetes, name="predict_diabetes"),
    path('signup', signup, name="signup"),
    path('login', login, name='login'),
    path('doctorpage', doctor_page, name='doctorpage'),
    path('assign-patient/<int:patient_id>', assign_patient, name='assign_patient'),
    path('wronguser',wronguser, name='wronguser')
]