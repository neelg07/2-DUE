// Log In Button pop up
const login = document.querySelector('.login-btn');

const loginContainer = document.querySelector('.login-container');

const indexHeader = document.querySelector('.index-header');

const closeLogin = document.querySelector('.close-login');

const logUser = document.getElementById('username');
const logPass = document.getElementById('password');


login.addEventListener('click', () => {
    
    loginContainer.classList.remove('hide');
    logUser.focus();
    indexHeader.classList.add('blur');

    regContainer.classList.add('hide');
});

closeLogin.addEventListener('click', () => {

    logUser.value = '';
    logPass.value = '';
    loginContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
});


const signUp = document.querySelector('.register-btn');
const regContainer = document.querySelector('.register-container')

const closeReg = document.querySelector('.close-register')

const regUser = document.getElementById('Username');
const regPass = document.getElementById('Password');
const regConfirm = document.getElementById('Verify-Pass');


signUp.addEventListener('click', () => {

    regContainer.classList.remove('hide');
    regUser.focus();
    indexHeader.classList.add('blur');

    loginContainer.classList.add('hide');
});

closeReg.addEventListener('click', () => {

    regUser.value = '';
    regPass.value = '';
    regConfirm.value = '';
    regContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
})
