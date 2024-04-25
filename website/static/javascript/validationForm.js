function validation() {
    var password = document.getElementById("password").value;
    var confirm = document.getElementById("confirm").value;
    var errorElement = document.getElementById("passwordError");
    var errorPlaceholder = document.getElementById("passwordErrorPlaceholder");

    if (password !== confirm) {
        errorElement.innerText = "Passwords do not match!";
        errorElement.classList.add("show"); // Show the error message
        errorPlaceholder.style.visibility = "visible"; // Show the placeholder
        return false;
    } else {
        errorElement.innerText = "";
        errorElement.classList.remove("show"); // Hide the error message
        errorPlaceholder.style.visibility = "hidden"; // Hide the placeholder
        return true;
    }
}

function checkEmailAvailability(email) {
    // You may need to adjust this URL according to your Flask route
    fetch(`/check_email_availability?email=${encodeURIComponent(email)}`)
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                document.getElementById("email-tooltip").style.display = "inline"; // Show tooltip
            } else {
                document.getElementById("email-tooltip").style.display = "none"; // Hide tooltip
            }
        });
}


                
