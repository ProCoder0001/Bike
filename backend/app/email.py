import os
import requests

from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Bike Service Booking")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")


def _send_email(receiver_email: str, subject: str, body: str):
    print("Sending email to:", receiver_email)

    payload = {
        "sender": {"name": SMTP_FROM_NAME, "email": SMTP_FROM_EMAIL},
        "to": [{"email": receiver_email}],
        "subject": subject,
        "textContent": body,
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=15)

    if response.status_code >= 300:
        raise Exception(f"Brevo API error {response.status_code}: {response.text}")

    print("Email sent successfully to:", receiver_email)


def send_reset_email(receiver_email: str, reset_link: str):
    try:
        body = f"""
Hello,

Click the link below to reset your password:

{reset_link}

If you didn't request a password reset, you can ignore this email.
"""
        _send_email(receiver_email, "Bike Service Password Reset", body)
    except Exception as e:
        print("EMAIL ERROR:", e)
        raise e


def send_booking_approved_email(receiver_email: str, customer_name: str, booking_code: str, service_date: str):
    try:
        body = f"""
Hi {customer_name},

Good news - your service booking #{booking_code} has been approved.
Your requested service date is {service_date}.

We'll email you again once your bike is ready for pickup.

Thanks,
Bike Service Booking Team
"""
        _send_email(receiver_email, f"Booking #{booking_code} Approved", body)
    except Exception as e:
        # Notification emails should never break the underlying status update.
        print("EMAIL ERROR (booking approved):", e)


def send_service_completed_email(receiver_email: str, customer_name: str, booking_code: str):
    try:
        body = f"""
Hi {customer_name},

Your bike is ready! Servicing for booking #{booking_code} is complete.

Please visit the service centre to collect your bike. If any payment is
still pending, you can pay by cash at pickup or add funds to your wallet
from the app beforehand.

Thanks,
Bike Service Booking Team
"""
        _send_email(receiver_email, f"Your bike is ready - Booking #{booking_code}", body)
    except Exception as a:
        print("EMAIL ERROR (service completed):", a)
