// Facebook login status check
function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

// Handle Facebook login status changes
function statusChangeCallback(response) {
    if (response.status === 'connected') {
        // User is logged in and authorized
        console.log('Welcome! Fetching your information....');
        fetchUserInfo(response.authResponse.accessToken);
    } else if (response.status === 'not_authorized') {
        // User is logged in but not authorized
        console.log('Please log into this app.');
    } else {
        // User is not logged in
        console.log('Please log into Facebook.');
    }
}

// Fetch user information after successful login
function fetchUserInfo(accessToken) {
    FB.api('/me', { fields: 'name,email,picture' }, function (response) {
        console.log('Successful login for: ' + response.name);
        // Here you can send the access token and user info to your backend
        // for authentication
        sendToBackend({
            accessToken: accessToken,
            userInfo: response
        });
    });
}

// Send user info to your backend
function sendToBackend(data) {
    fetch('/auth/facebook/callback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/'; // Redirect to home page after successful login
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Add Facebook login button click handler
document.addEventListener('DOMContentLoaded', function () {
    const fbLoginBtn = document.getElementById('fb-login-button');
    if (fbLoginBtn) {
        fbLoginBtn.addEventListener('click', function () {
            FB.login(function (response) {
                if (response.authResponse) {
                    checkLoginState();
                }
            }, { scope: 'public_profile,email' });
        });
    }
});
