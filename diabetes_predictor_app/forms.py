# diabetes_predictor_app/forms.py
from django import forms

class DiabetesForm(forms.Form):
    Pregnancies = forms.IntegerField(
        label='Number of Pregnancies',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 2'})
    )
    Glucose = forms.FloatField(
        label='Glucose Level (mg/dL)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 120'})
    )
    BloodPressure = forms.FloatField(
        label='Blood Pressure Diastolic (mmHg)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 80'})
    )
    SkinThickness = forms.FloatField(
        label='Skin Thickness (mm)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 25'})
    )
    Insulin = forms.FloatField(
        label='Insulin Level (mu U/mL)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 85'})
    )
    BMI = forms.FloatField(
        label='BMI (kg/m²)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 24.5'})
    )
    DiabetesPedigreeFunction = forms.FloatField(
        label='Diabetes Pedigree Function',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 0.45'})
    )
    Age = forms.IntegerField(
        label='Age (years)',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 45'})
    )
