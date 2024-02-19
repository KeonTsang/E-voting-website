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
