// Log In Button pop up
const login = document.querySelector('.login-btn');
const loginContainer = document.querySelector('.login-container');
const indexHeader = document.querySelector('.index-header');
const closeLogin = document.querySelector('.close-login');

const logUser = document.getElementById('username');
const logPass = document.getElementById('password');
const logPassCheck = document.querySelector('.show-pass');


login.addEventListener('click', () => {
    
    loginContainer.classList.remove('hide');
    logUser.focus();

    closeReg.click();
    indexHeader.classList.add('blur');
});

closeLogin.addEventListener('click', () => {

    logUser.value = '';
    logPass.value = '';
    logPassCheck.checked = false;

    loginContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
});


// Sign Up button popup
const signUp = document.querySelector('.register-btn');
const regContainer = document.querySelector('.register-container')
const closeReg = document.querySelector('.close-register')

const regUser = document.getElementById('Username');
const regPass = document.getElementById('Password');
const regConfirm = document.getElementById('Verify-Pass');
const regPassCheck = document.querySelector('.reg-show-pass');

const regBtn = document.querySelector('.register-submit');


signUp.addEventListener('click', () => {

    regContainer.classList.remove('hide');
    regUser.focus();

    closeLogin.click();
    indexHeader.classList.add('blur');
});

closeReg.addEventListener('click', () => {

    regUser.value = '';
    regPass.value = '';
    regConfirm.value = '';
    regPassCheck.checked = false;

    regContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
    regUser.removeAttribute('style');
});

// Sign up info verification
regUser.addEventListener('keypress', () => {

    if (regUser.value.length < 2 || regUser.value.length > 17) {
        regUser.setAttribute('style', 'border: 1px solid red;');
        regBtn.disabled = true;
    } else {
        regUser.removeAttribute('style');
        regBtn.disabled = false;
    }
});

regUser.addEventListener('keydown', function(event) {

    switch (event.key) {
        case 'Backspace':
        case 'Delete':
            if (regUser.value.length === 3) {
                regUser.setAttribute('style', 'border: 1px solid red;');
                regBtn.disabled = true;
            } else if (regUser.value.length === 19) {
                regUser.removeAttribute('style');
                regBtn.disabled = false;
            }
    }
});

/*
regPass.addEventListener('keypress', () => {
    
}) */

// Show password function
logPassCheck.addEventListener('click', () => {

    if (logPassCheck.checked === true) {
        logPass.type = 'text';
    } else {
        logPass.type = 'password';
    }
});

regPassCheck.addEventListener('click', () => {

    if (regPassCheck.checked === true) {
        regPass.type = 'text';
        regConfirm.type = 'text';
    } else {
        regPass.type = 'password';
        regConfirm.type = 'password';
    }
});