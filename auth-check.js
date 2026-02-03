// auth-check.js
// Check authentication on all pages

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    auth.onAuthStateChanged(async (user) => {
        const currentPage = window.location.pathname;
        
        if (!user && currentPage.includes('points.html')) {
            // Redirect to login if trying to access points page without login
            window.location.href = 'login.html';
        } else if (user && (currentPage.includes('login.html') || currentPage.includes('register.html'))) {
            // Redirect to home if already logged in
            window.location.href = 'index.html';
        }
    });
});