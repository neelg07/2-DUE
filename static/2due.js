// 2-DUE Daily
const dailyForm = document.querySelector('.daily');
const frequency = document.querySelector('.select');

dailyForm.addEventListener('submit', (event) => {

    if (frequency.value == 'select') {
        frequency.setAttribute('style', 'border: 2px solid red;')
        event.preventDefault();
    } else {
        frequency.removeAttribute('style');
    }
});

frequency.addEventListener('click', () => {

    frequency.removeAttribute('style');
});
