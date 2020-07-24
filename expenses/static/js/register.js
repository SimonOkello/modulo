const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailFeedBackArea = document.querySelector(".invalidEmail_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPassword = document.querySelector(".showPassword")

// Username Validation
usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  usernameSuccessOutput.style.display = "block";
  usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

  feedBackArea.style.display = "none";
  usernameField.classList.remove("is-invalid");

  if (usernameVal.length > 0) {
    fetch("/auth/validate_username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        usernameSuccessOutput.style.display = "none";

        if (data.username_error) {
          feedBackArea.style.display = "block";
          usernameField.classList.add("is-invalid");
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
        }
      });
  }
});

// Email Validation
emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailSuccessOutput.style.display = "block";
  emailSuccessOutput.textContent = `Checking ${emailVal}`;

  emailFeedBackArea.style.display = "none";
  emailField.classList.remove("is-invalid");

  if (emailVal.length > 0) {
    fetch("/auth/validate_email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        emailSuccessOutput.style.display = "none";
        if (data.email_error) {
          emailFeedBackArea.style.display = "block";
          emailField.classList.add("is-invalid");
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        }
      });
  }
});
 
const handleToggleInput = (e)=>{
    if(showPassword.textContent==="Show"){
        showPassword.textContent="Hide"
        passwordField.setAttribute("type", "text");
    }else{
        showPassword.textContent="Show"
        passwordField.setAttribute("type", "password");
    }

};

showPassword.addEventListener("click", handleToggleInput);

