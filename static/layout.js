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

const regBtn = document.getElementById('register-submit');


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
function checkRegUser() {
    if (regUser.value.length <= 3 || regUser.value.length > 19) {
        return false;
    } else {
        return true;
    }
};

function checkRegPass() {
    if (regPass.value.length <= 3 || regPass.value.length > 19) {
        return false;
    } else {
        return true;
    }
};

function checkPassMatch() {
    if (regPass.value !== regConfirm.value) {
        return false;
    } else {
        return true;
    }
};


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
            if (!checkRegUser()) {
                regUser.setAttribute('style', 'border: 1px solid red;');
                regBtn.disabled = true;
            } else {
                regUser.removeAttribute('style');
                regBtn.disabled = false;
            }
    }
});


regPass.addEventListener('keypress', () => {
    if (regPass.value.length < 2 || regPass.value.length > 17) {
        regPass.setAttribute('style', 'border: 1px solid red;');
        regBtn.disabled = true;
    } else {
        regPass.removeAttribute('style');
        regBtn.disabled = false;
    }
});

regPass.addEventListener('keydown', function(event) {

    switch (event.key) {
        case 'Backspace':
        case 'Delete':
            if (!checkRegPass()) {
                regPass.setAttribute('style', 'border: 1px solid red;');
                regBtn.disabled = true;
            } else {
                regPass.removeAttribute('style');
                regBtn.disabled = false;
            }
    }
});


const regForm = document.querySelector('.register-form');

regForm.addEventListener('submit', (event) => {

    if (!checkPassMatch()) {
        alert('Passwords must match!');
        event.preventDefault();
    }
    if (regUser.value === '') {
        alert('Must enter username');
        event.preventDefault();
    }
    if (regPass.value === '') {
        alert('Must enter password');
        event.preventDefault();
    }
});


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


// Forgot Password Popup Logic

const forgotPop = document.querySelector('.forgot-pop');
const closeForgot = document.querySelector('.close-forgot');
const forgotPass = document.querySelector('.forgot-pass');
const codeInput = document.getElementById('forgot-code');
const forgotUser = document.getElementById('forgot-user');


forgotPass.addEventListener('click', () => {

    forgotPop.classList.remove('hide');
    closeLogin.click();
    indexHeader.classList.add('blur');
    forgotUser.focus();
});

closeForgot.addEventListener('click', () => {

    forgotPop.classList.add('hide');
    indexHeader.classList.remove('blur');
    codeInput.value = '';
});


// Forgot Password Show Password Checkbox
const resetPassShow = document.querySelector('.reset-show-pass');
const resetNewPass = document.getElementById('pass-reset');
const resetNewConfirm = document.getElementById('verify-pass-reset');
const resetSubmit = document.getElementById('forgot-password');


resetPassShow.addEventListener('click', () => {

    if (resetPassShow.checked === true) {

        resetNewPass.type = 'text';
        resetNewConfirm.type = 'text';
    } else {

        resetNewPass.type = 'password';
        resetNewConfirm.type = 'password';
    }
});