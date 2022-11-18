// Change Username Popup
const accountHeader = document.querySelector('.account-header');

const userPop = document.querySelector('.username-pop');
const closeUser = document.querySelector('.close-register');
const userBtn = document.querySelector('.change-user');
const newUser = document.getElementById('new-user');


function disableButtons() {

    userBtn.disabled = true;
    passBtn.disabled = true;
    deleteAccount.disabled = true;

    accountHeader.classList.add('blur');
};

function enableButtons() {

    userBtn.disabled = false;
    passBtn.disabled = false;
    deleteAccount.disabled = false;

    accountHeader.classList.remove('blur');
};



userBtn.addEventListener('click', () => {

    userPop.classList.remove('hide');
    newUser.focus();
    disableButtons();
});

closeUser.addEventListener('click', () => {

    userPop.classList.add('hide');
    enableButtons();
    newUser.value = '';
});


const submitUser = document.getElementById('change-user');

submitUser.addEventListener('click', (event) => {

    if (newUser.value.length < 3) {
        alert('Username must be >= 3 characters!');
        event.preventDefault();
    }
    if (newUser.value.length > 18) {
        alert('Username must be <= 18 characters!');
        event.preventDefault();
    }
});

// Change Password Popup
const passPop = document.querySelector('.password-pop');
const passBtn = document.querySelector('.change-pass');
const closePass = document.querySelector('.close-pass');
const newPass = document.getElementById('new-pass');
const confirmPass = document.getElementById('confirm-new-pass');
const showPass = document.querySelector('.show-pass');


passBtn.addEventListener('click', () => {

    passPop.classList.remove('hide');
    newPass.focus();
    disableButtons();
});

closePass.addEventListener('click', () => {

    passPop.classList.add('hide');
    enableButtons();
    newPass.value = '';
    confirmPass.value = '';
});

showPass.addEventListener('click', () => {

    if (showPass.checked === true) {
        newPass.type = 'text';
        confirmPass.type = 'text';
    } else {
        newPass.type = 'password';
        confirmPass.type = 'password';
    }
});


const submitPass = document.getElementById('change-pass');


submitPass.addEventListener('click', (event) => {

    if (newPass.value !== confirmPass.value) {
        alert('Passwords Must Match!');
        event.preventDefault();
    }
    if (newPass.value === '') {
        alert('Must enter a new password !');
        event.preventDefault();
    }
    if (newPass.value.length < 3 || newPass.value.length > 18) {
        alert('Password length must be between 3 and 18 characters!');
        event.preventDefault();
    }
});

// Delete Account 
const deleteAccount = document.querySelector('.delete-account');


