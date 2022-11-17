// Change Username Popup
const accountHeader = document.querySelector('.account-header');

const userPop = document.querySelector('.username-pop');
const closeUser = document.querySelector('.close-register');

const userBtn = document.querySelector('.change-user');


function disableButtons() {

    userBtn.disabled = true;
    passBtn.disabled = true;
    deleteAccount.disabled = true;
};

function enableButtons() {

    userBtn.disabled = false;
    passBtn.disabled = false;
    deleteAccount.disabled = false;
};


userBtn.addEventListener('click', () => {

    accountHeader.classList.add('blur');
    userPop.classList.remove('hide');

    disableButtons();
});

closeUser.addEventListener('click', () => {

    accountHeader.classList.remove('blur');
    userPop.classList.add('hide');

    enableButtons();
});


// Change Password Popup
const passPop = document.querySelector('.password-pop');
const passBtn = document.querySelector('.change-pass')


// Delete Account 
const deleteAccount = document.querySelector('.delete-account');

