function validation(){
  var password = document.getElementById("password").value;
  var confirm = document.getElementById("confirm").value;
  var errorElement = document.getElementById("passwordError");

  if (password !== confirm) {
      errorElement.innerText = "Passwords do not match!";
      return false;
  } else {
      errorElement.innerText = "";
      return true;
  }
}
