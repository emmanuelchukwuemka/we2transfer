# Flask Form Submission App

This is a Flask application that serves a web form and handles form submissions by sending the data via email.

## Features

- Simple web form interface
- Email notification on form submission
- Responsive design
- Dual email sender for reliability

## Deployment to Render

This application is configured for deployment to Render with the included `render.yaml` file.

### Environment Variables

Set these environment variables in your Render dashboard:

- `SENDER_EMAIL` - Primary sender email address (required)
- `SENDER_EMAIL_BACKUP` - Backup sender email address (optional)
- `SENDER_PASSWORD` - Sender email password or app password (required)
- `RECEIVER_EMAIL` - Email address to receive form submissions (required)
- `SMTP_SERVER` - SMTP server (default: smtp.gmail.com)
- `SMTP_PORT` - SMTP port (default: 587)

**Important:** For Gmail, you should use an App Password instead of your regular password. Generate one in your Google Account settings.

### Deploy Steps

1. Fork this repository or push it to GitHub/GitLab
2. Create a new Web Service on Render
3. Connect your repository
4. Set the build command to `pip install -r requirements.txt`
5. Set the start command to `gunicorn --bind 0.0.0.0:$PORT app:app`
6. Add the required environment variables
7. Deploy!

## Local Development

To run locally:

```bash
pip install -r requirements.txt
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
export RECEIVER_EMAIL=receiver-email@gmail.com
python app.py
```

Visit `http://localhost:8000` in your browser.

## How It Works

1. The application serves `index.html` as the main page
2. When users submit the form, data is sent to `/submit` endpoint
3. The Flask backend captures the form data and sends it via email
4. Success response is returned to the client

## Security Notes

- Form data is sent via email
- No database storage
- Email credentials should be kept secure
- Use App Passwords for Gmail instead of regular passwords