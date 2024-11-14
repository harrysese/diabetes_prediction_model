# diabetes_predictor_app/forms.py
from django import forms

class DiabetesForm(forms.Form):
    Pregnancies = forms.IntegerField(
        label='',  # Removes label
        widget=forms.NumberInput(attrs={'placeholder': 'Number of Pregnancies'})
    )
    Glucose = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Glucose Level'})
    )
    BloodPressure = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Blood Pressure'})
    )
    SkinThickness = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Skin Thickness'})
    )
    Insulin = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Insulin Level'})
    )
    BMI = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'BMI'})
    )
    DiabetesPedigreeFunction = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Diabetes Pedigree Function'})
    )
    Age = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Age'})
    )
