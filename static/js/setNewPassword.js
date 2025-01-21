const passwordField = document.querySelector('#passwordField');
const passwordField1 = document.querySelector('#passwordField1');
const showPasswordToggel = document.querySelector('.showPasswordToggel');
const submitBtn = document.querySelector('.submit-btn');




// --------------- Show Password Validation --------------- 

// if (passwordField === passwordField1) {
    
// }

const handleToggelInput = (e) =>{
    if(showPasswordToggel.textContent === 'SHOW'){
        showPasswordToggel.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
        passwordField1.setAttribute("type", "text");
    }else{
        showPasswordToggel.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
        passwordField1.setAttribute("type", "password");
    }
}
showPasswordToggel.addEventListener('click',handleToggelInput);
