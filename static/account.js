// Change Username Popup
const accountHeader = document.querySelector('.account-header');

const userPop = document.querySelector('.username-pop');
const closeUser = document.querySelector('.close-register');

const userBtn = document.querySelector('.change-user');


userBtn.addEventListener('click', () => {

    accountHeader.classList.add('blur');
    userPop.classList.remove('hide');
});

closeUser.addEventListener('click', () => {

    accountHeader.classList.remove('blur');
    userPop.classList.add('hide');
});