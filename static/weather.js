// Close weather button 
const city = document.querySelector('.city');
const forecast = document.querySelector('.forecast');
const temp = document.querySelector('.temp');
const info = document.querySelector('.weather-info');
const icon = document.querySelector('.weather-icon');
const img = document.querySelector('.icon');

const closeWeather = document.querySelector('button.close-weather');

closeWeather.addEventListener('click', () => {

    city.textContent = '';
    forecast.textContent = '';
    temp.textContent = '';
    info.textContent = '';
    icon.removeChild(img);
});