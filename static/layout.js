// Log In Button pop up
let login = document.querySelector('.login-btn');

let loginContainer = document.querySelector('.login-container');

let indexHeader = document.querySelector('.index-header');

let closeLogin = document.querySelector('.close-login');


login.addEventListener('click', () => {
    
    loginContainer.classList.remove('hide');
    indexHeader.classList.add('blur');
});

closeLogin.addEventListener('click', () => {

    loginContainer.classList.add('hide');
    indexHeader.classList.remove('blur');
});