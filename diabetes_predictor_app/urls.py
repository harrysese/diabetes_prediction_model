from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('wronguser',wronguser, name='wronguser'),
      # Password reset URLs
      
      
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',html_email_template_name='registration/password_reset_email.html'

    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]