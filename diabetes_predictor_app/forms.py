from django import forms

class DiabetesForm(forms.Form):
    Name = forms.CharField(
        label='Name',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    Pregnancies = forms.IntegerField(
        label='',  # Removes label
        widget=forms.NumberInput(attrs={
            'placeholder': 'Number of Pregnancies (count)'
        })
    )
    Glucose = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Glucose Level (mg/dL)'
        })
    )
    BloodPressure = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Blood Pressure (mmHg)'
        })
    )
    SkinThickness = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Skin Thickness (mm)'
        })
    )
    Insulin = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Insulin Level (IU/mL)'
        })
    )
    BMI = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'BMI (kg/m²)'
        })
    )
    DiabetesPedigreeFunction = forms.FloatField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Diabetes Pedigree Function (relative risk)'
        })
    )
    Age = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Age (years)'
        })
    )
