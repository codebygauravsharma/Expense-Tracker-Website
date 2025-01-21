const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const passwordField = document.querySelector('#passwordField');
const EmailfeedBackArea = document.querySelector('.emailfeedbackArea');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');
const showPasswordToggel = document.querySelector('.showPasswordToggel');
const submitBtn = document.querySelector('.submit-btn');



// --------------- Show Password Validation --------------- 
const handleToggelInput = (e) =>{
    if(showPasswordToggel.textContent === 'SHOW'){
        showPasswordToggel.textContent = "HIDE";

        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggel.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}
showPasswordToggel.addEventListener('click',handleToggelInput);



// --------------- Email Validation --------------- 
emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailSuccessOutput.style.display = 'block';
    emailSuccessOutput.textContent = `Checking ${emailVal}`;
    emailField.classList.remove("is-invalid");
    EmailfeedBackArea.style.display = "none";
    
    // console.log("usernameVal",usernameVal)

    if(emailVal.length > 0) {
        fetch("/authentication/validate-email",{
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email: emailVal}), 
            method: "POST",
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("data",data);
        emailSuccessOutput.style.display = 'none';
        if(data.email_error){
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            EmailfeedBackArea.style.display = "block";
            EmailfeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        }else{
            submitBtn.removeAttribute("disabled");
        }
    });
    }
});

// --------------- Username Validation --------------- 
usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = 'block';

    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
        
    // console.log("usernameVal",usernameVal)

    if(usernameVal.length > 0) {
        fetch("/authentication/validate-username",{
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({username: usernameVal}), 
            method: "POST",
    })
    .then((res) => res.json())
    .then((data) => {
        usernameSuccessOutput.style.display = 'none';
        if(data.username_error){
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display = "block";
            feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            submitBtn.disabled = true;
        }else{
            submitBtn.removeAttribute("disabled");
        }
    });
    }
});