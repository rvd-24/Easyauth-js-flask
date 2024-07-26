document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const getUserInfoBtn = document.getElementById('getUserInfoBtn');
    const userInfoDiv = document.getElementById('userInfo');

    loginBtn.addEventListener('click', () => {
        // Redirect to the login page
        window.location.href = '/.auth/login/aad';
    });

    getUserInfoBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/user');
            const data = await response.json();
            userInfoDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        } catch (error) {
            console.error('Error:', error);
            userInfoDiv.innerHTML = 'Error fetching user info';
        }
    });

    // Check if user is authenticated
    fetch('/.auth/me')
        .then(response => response.json())
        .then(data => {
            if (data.clientPrincipal) {
                loginBtn.style.display = 'none';
                getUserInfoBtn.style.display = 'block';
            }
        })
        .catch(error => console.error('Error:', error));
});