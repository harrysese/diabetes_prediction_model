from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_remark_email(patient, doctor_name, remark, email):
    subject = f'New Remark from Dr. {doctor_name}'
    from_email = 'usepredicare@gmail.com'
    to_email = [email]
    
    context = {
        'doctor_name': doctor_name,
        'patient_name': patient.user.first_name,
        'remark': remark
    }
    
    # Plain text version
    text_content = f"""Dear {patient.user.first_name},
    
Dr. {doctor_name} has left a new remark for you:

"{remark}"

Please log in to your DiaCare account to view details or reply.

Best regards,
DiaCare Team
"""
    
    # HTML version
    html_content = render_to_string('email/remark_email.html', context)
    
    # Create email with proper MIME type
    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_email
    )
    email_msg.attach_alternative(html_content, "text/html")
    
    # Set important headers for email clients
    email_msg.content_subtype = "html"
    email_msg.mixed_subtype = 'related'
    
    try:
        email_msg.send(fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {str(e)}")