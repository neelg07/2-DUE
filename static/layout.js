// Log In Button pop up
let login = document.querySelector('.login-btn');

let loginContainer = document.querySelector('.login-container');

let indexHeader = document.querySelector('.index-header');

let closeLogin = document.querySelector('.close-login');

let logUser = document.getElementById('username');
let logPass = document.getElementById('password');


login.addEventListener('click', () => {
    
    loginContainer.classList.remove('hide');
    logUser.focus();
    indexHeader.classList.add('blur');
});

closeLogin.addEventListener('click', () => {

    logUser.value = '';
    logPass.value = '';
    loginContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
});