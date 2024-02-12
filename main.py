from flask import Flask, request, redirect, render_template, flash, url_for
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import ssl

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fr')
def home_fr():
    return render_template('index_fr.html')


@app.route('/send_email', methods=['POST'])
def handle_form_submission():
    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')  # Capture the phone number
    message = request.form.get('message')

    # Construct email content
    email_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

    # Send email
    send_email(email_body)

    # Flash a thank-you message
    flash('Thank you for your message! We will get back to you soon.')

    # Redirect to the home page
    return redirect(url_for('home'))

def send_email(body):
    MY_EMAIL = os.getenv('my_email')
    MY_EMAIL_PASS = os.getenv('password')
    SENT_EMAIL_TO = os.getenv('send_to')

    em = EmailMessage()
    em['From'] = MY_EMAIL
    em['To'] = SENT_EMAIL_TO
    em['Subject'] = 'New Contact Form Submission'
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(MY_EMAIL, MY_EMAIL_PASS)
        smtp.send_message(em)


if __name__ == '__main__':
    app.run(debug=True)
