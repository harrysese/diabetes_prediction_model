from .views import *
from django.urls import path

urlpatterns=[
    path('', predict_diabetes, name="predict_diabetes"),
    path('signup', signup, name="signup"),
    path('login', login, name='login'),
    path('doctor', doctor_page, name='doctor'),
    path('assign-patient/<int:patient_id>', assign_patient, name='assign_patient'),
    path('patient-detail/<int:patient_id>', patient_detail, name='patient_detail'),
    path('submit-remark/<int:patient_id>', submitremark, name='submit_remark'),
    path('wronguser',wronguser, name='wronguser')
]