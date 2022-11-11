// Log In Button pop up
let login = document.querySelector('.login-btn');

let loginContainer = document.querySelector('.login-container');

let indexHeader = document.querySelector('.index-header');

login.addEventListener('click', () => {
    
    loginContainer.classList.remove('hide');
    indexHeader.classList.add('blur');
});