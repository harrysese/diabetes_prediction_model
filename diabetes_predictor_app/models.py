from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Additional fields for your custom user model can be defined here.
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')])
    
    # Overriding `groups` and `user_permissions` to avoid clashes
    groups = models.ManyToManyField(
        Group, 
        related_name='diabetes_predictor_user_set', 
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups."
    )
    
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='diabetes_predictor_user_permissions_set', 
        blank=True,
        help_text="Specific permissions for this user."
    )
    
    def __str__(self):
        return self.username

class DoctorProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctorprofile")
    license_number=models.IntegerField()
    specialisation=models.TextField(max_length=50)
    def __str__(self):
        return self.user.first_name
class Patient(models.Model):
    Name=models.CharField(max_length=40)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    Pregnancies=models.IntegerField(null=True, blank=True)
    Glucose=models.FloatField(null=True, blank=True)
    BloodPressure = models.FloatField(null=True, blank=True)
    SkinThickness = models.FloatField(null=True, blank=True)
    BMI = models.FloatField(null=True, blank=True)
    Insulin = models.FloatField(null=True, blank=True)
    Age=models.IntegerField(null=True, blank=True)
    DiabetesPedigreeFunction=models.FloatField(null=True, blank=True)
    Result=models.TextField(max_length=30,null=True, blank=True)
    remark=models.TextField(max_length=90, null=True, blank=True)
    Prediction=models.FloatField(max_length=5,null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self:object) -> str:
        return f"{self.Name}"