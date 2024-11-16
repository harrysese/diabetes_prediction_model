from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_remark_email(patient, doctor_name, remark):
    # Define the subject and recipient(s)
    subject = f'New Remark from Dr. {doctor_name}'
    from_email = 'usepredicare@gmail.com'
    to_email = ["tokonisese@gmail.com"]
    
    # Define the context for the template
    context = {
        'doctor_name': doctor_name,
        'patient_name': patient.user.first_name,
        'remark': remark
    }
    
    # Render both plain text and HTML versions of the email
    text_content = f"Dear {patient.user.first_name},\n\nDr. {doctor_name} has left a remark for you:\n\n{remark}"
    html_content = render_to_string('email/remark_email.html', context)
    
    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send()

