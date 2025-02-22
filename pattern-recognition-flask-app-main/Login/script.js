document.addEventListener("DOMContentLoaded", function () {
    // ✅ LOGIN FORM HANDLING
    document.getElementById("loginForm")?.addEventListener("submit", function (event) {
        event.preventDefault();
        
        let email = document.getElementById("loginEmail").value.trim();
        let password = document.getElementById("loginPassword").value.trim();
        
        // Get stored user data from localStorage
        let storedEmail = localStorage.getItem("userEmail")?.trim();
        let storedPassword = localStorage.getItem("userPassword")?.trim();

        // Debugging logs
        console.log("Entered Email:", email);
        console.log("Stored Email:", storedEmail);
        console.log("Entered Password:", password);
        console.log("Stored Password:", storedPassword);

        if (!storedEmail || !storedPassword) {
            alert("No registered user found. Please sign up first.");
            return;
        }

        if (email === storedEmail && password === storedPassword) {
            alert("Login Successful!");
            window.location.href = "dashboard.html"; // Redirect to dashboard
        } else {
            alert("Invalid email or password!");
        }
    });

    // ✅ REGISTER FORM HANDLING
    document.getElementById("registerForm")?.addEventListener("submit", function (event) {
        event.preventDefault();

        let username = document.getElementById("username").value.trim();
        let email = document.getElementById("registerEmail").value.trim();
        let password = document.getElementById("registerPassword").value.trim();
        let confirmPassword = document.getElementById("confirmPassword").value.trim();

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Check if email already exists
        let existingEmail = localStorage.getItem("userEmail");
        if (existingEmail === email) {
            alert("This email is already registered. Please log in.");
            return;
        }

        // Store user details in localStorage
        localStorage.setItem("username", username);
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userPassword", password);

        alert("Registration Successful! You can now log in.");
        window.location.href = "index.html"; // Redirect to login page
    });
});
