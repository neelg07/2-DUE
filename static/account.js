// Change Username Popup
const accountHeader = document.querySelector('.account-header');

const userPop = document.querySelector('.username-pop');
const closeUser = document.querySelector('.close-register');

const userBtn = document.querySelector('.change-user');


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
    disableButtons();
});

closeUser.addEventListener('click', () => {

    userPop.classList.add('hide');
    enableButtons();
});



// Change Password Popup
const passPop = document.querySelector('.password-pop');
const passBtn = document.querySelector('.change-pass');
const closePass = document.querySelector('.close-pass');


passBtn.addEventListener('click', () => {

    passPop.classList.remove('hide');
    disableButtons();
});

closePass.addEventListener('click', () => {

    passPop.classList.add('hide');
    enableButtons();
});

// Delete Account 
const deleteAccount = document.querySelector('.delete-account');


