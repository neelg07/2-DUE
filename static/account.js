// Change Username Popup
const accountHeader = document.querySelector('.account-header');

const userPop = document.querySelector('.username-pop');
const closeUser = document.querySelector('.close-register');
const userBtn = document.querySelector('.change-user');
const newUser = document.getElementById('new-user');

// Functions to disable and enable buttons with popups open
function disableButtons() {

    userBtn.disabled = true;
    passBtn.disabled = true;
    delAccount.disabled = true;

    accountHeader.classList.add('blur');
};

function enableButtons() {

    userBtn.disabled = false;
    passBtn.disabled = false;
    delAccount.disabled = false;

    accountHeader.classList.remove('blur');
};


// Open and close change user popup
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

// Change user submit button
const submitUser = document.getElementById('change-user');

submitUser.addEventListener('click', (event) => {

    if (newUser.value.length < 3 || newUser.value.length > 18) {
        alert('Username must be between 3 and 18 characters!');
        event.preventDefault();
    } else {
        alert('Username Changed Successfully')
    }
});


// Change Password Popup
const passPop = document.querySelector('.password-pop');
const passBtn = document.querySelector('.change-pass');
const closePass = document.querySelector('.close-pass');
const newPass = document.getElementById('new-pass');
const confirmPass = document.getElementById('confirm-new-pass');
const showPass = document.querySelector('.show-pass');

// Open and close change password popup
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

// Show password checkbox 
showPass.addEventListener('click', () => {

    if (showPass.checked === true) {
        newPass.type = 'text';
        confirmPass.type = 'text';
    } else {
        newPass.type = 'password';
        confirmPass.type = 'password';
    }
});


// Change password submit button
const submitPass = document.getElementById('change-pass');

submitPass.addEventListener('click', (event) => {

    if (newPass.value !== confirmPass.value) {
        alert('Passwords Must Match!');
        event.preventDefault();
        return;
    }
    if (newPass.value === '') {
        alert('Must enter a new password !');
        event.preventDefault();
        return;
    }
    if (newPass.value.length < 3 || newPass.value.length > 18) {
        alert('Password length must be between 3 and 18 characters!');
        event.preventDefault();
    } else {
        alert('Password Changed Successfully')
    }
});


// Delete Account 
const delAccount = document.querySelector('.delete-account');
const delPop = document.querySelector('.delete-pop');
const delClose = document.querySelector('.close-delete');
const delText = document.querySelector('.del-text');
const delSubmit = document.getElementById('delete-account');


// Open and close delete account popup
delAccount.addEventListener('click', () => {

    delPop.classList.remove('hide');
    delText.focus();
    disableButtons();
});

delClose.addEventListener('click', () => {

    delText.value = '';
    delPop.classList.add('hide');
    enableButtons();
});


// Delete account submit button 
delSubmit.addEventListener('click', (event) => {

    if (delText.value !== 'DELETE') {

        alert('Invalid Submission');
        event.preventDefault();
        delText.value = '';
        delText.focus();
    }
});
