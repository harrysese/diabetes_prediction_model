# Generated by Django 5.1.1 on 2024-11-13 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_predictor_app', '0002_patient_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='BMI',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='BloodPressure',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='DiabetesPedigreeFunction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Glucose',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Insulin',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Prediction',
            field=models.FloatField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Pregnancies',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Result',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='SkinThickness',
            field=models.FloatField(blank=True, null=True),
        ),
    ]