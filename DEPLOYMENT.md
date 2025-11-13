# Deployment Guide for Render

This document explains how to deploy this PHP form submission application to Render.

## Files Prepared for Deployment

1. **[app.php](file:///c:/xampp/htdocs/wetransfer/app.php)** - Main application file with form handling and email functionality
2. **[render.yaml](file:///c:/xampp/htdocs/wetransfer/render.yaml)** - Render deployment configuration
3. **[composer.json](file:///c:/xampp/htdocs/wetransfer/composer.json)** - PHP dependencies configuration
4. **[.gitignore](file:///c:/xampp/htdocs/wetransfer/.gitignore)** - Updated to properly ignore PHP dependencies
5. **[.env.example](file:///c:/xampp/htdocs/wetransfer/.env.example)** - Example environment variables
6. **[README.md](file:///c:/xampp/htdocs/wetransfer/README.md)** - Project documentation
7. **src/** - Directory for PHP classes to satisfy autoloading

## Deployment Steps

1. Push this code to a GitHub or GitLab repository
2. Sign up/in to Render
3. Create a new Web Service
4. Connect your repository
5. Render will automatically detect the [render.yaml](file:///c:/xampp/htdocs/wetransfer/render.yaml) file and use its configuration
6. Add the required environment variables in the Render dashboard:
   - `SENDER_EMAIL`
   - `SENDER_EMAIL_BACKUP`
   - `SENDER_PASSWORD`
   - `RECEIVER_EMAIL`
   - `SMTP_SERVER` (optional, defaults to smtp.gmail.com)
   - `SMTP_PORT` (optional, defaults to 587)
7. Deploy the application

## How It Works

Render will:
1. Run `composer install` as the build command
2. Run `php -S 0.0.0.0:$PORT app.php` as the start command
3. Automatically set the `$PORT` environment variable

## Environment Variables

Make sure to configure these environment variables in your Render dashboard:

```
SENDER_EMAIL=your-primary-email@gmail.com
SENDER_EMAIL_BACKUP=your-backup-email@gmail.com
SENDER_PASSWORD=your-app-password
RECEIVER_EMAIL=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Notes

- The application uses PHP's built-in server for simplicity
- Form submissions are sent via email using PHP's `mail()` function
- The application has a fallback mechanism with a backup email sender
- All sensitive data should be stored in Render's environment variables, not in the code