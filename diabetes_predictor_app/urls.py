from .views import *
from django.urls import path

urlpatterns=[
    path('', index, name="index"),
    path('signup', signup, name="signup"),
    path('login', login, name='login'),
    path('predict', predict_diabetes, name="predict"),
    path('patient', patient, name='patient_dashboard'),
    path('doctor', doctor_page, name='doctor'),
    path('logout', logout, name='logout'),
    path('assign-patient/<int:patient_id>', assign_patient, name='assign_patient'),
    path('patient-detail/<int:patient_id>', patient_detail, name='patient_detail'),
    path('result', result, name='patient_result'),
    path('submit-remark/<int:patient_id>', submitremark, name='submit_remark'),
    path('wronguser',wronguser, name='wronguser')
]