# 2-DUE
Personalized To-Do List Web Application

### Video Demo: <https://youtu.be/Rx2yBMKSwek>

# Description: 

## Why? 
I am creating this to submit as my final project for Harvard's CS50x online course. In addition to material learned in the course, I will also be using the Web Development skills I honed in the past few weeks through 'The Odin Project' to create a well-developed web application with no guidance or "rules" to follow. This will essentially be a big test on my abilities and personal development as a programmer. 

## What is 2-DUE?
As stated before, 2-DUE is a web application designed to act like a To-Do list. There is strong evidence found in research that supports the claim that time-boxing and planning out a schedule for your day can improve the likelihood of actually following through and committing to said goals. 

Consistency and repetitive action tend to turn into strong habits over time. Realizing and leveraging this phenomenon can yield large-scale results over a long enough time. As a programmer taking the self-taught route, I try to maximize my probability of achieving goals using this same process and figured a to-do list web app would be a great idea for a project that will test and develop certain skills needed in web development.  

## Software Used
The following softwares are used to build this project:

    - Python/Flask
    - HTML/Jinja 2
    - CSS/Bootstrap
    - Vanilla JavaScript

## Welcome / Sign Up Page
The initial sign in page took some inspiration for its design from the CS50 finance assignment's web page, but was made from scratch by myself using HTML and CSS. Javascript was used to implement sign up and login forms to show on the screen in the form of popups/modals. It featured a blurring effect on the background if a popup was opened. Opening the log in form by clicking the appropriate button would automatically close the sign up form if open and vice versa. Forms would also reset all user input if closed while partially complete without hitting the submit button. 

The 'show password' input allows users to change their password form control to change from type=password to type=text to be able to control the visibility/privacy of inputting a password. A 'forgot password' link was implemented to allow users to change their password. This is done by providing the user with a randomly-generated 4-digit numeric code that the user must remember and input to create the new password and be able to login. Unfortunately, if the user forgets both their password and security code, their account would be locked forever and they would have to create a new one. This is because I chose not to add 2-factor authentification for this web app. Finally, I learned good bit about the use of box-shadow and text-shadow properties in CSS to implement the effect of outlining letters and making pseudo-3D containers for multi-purpose aesthetic use.

## Weather
Upon a user's first time sign-up, a pop-up displaying the user's unique security code and instructions for its use is automatically open. When closing this popup, the user is in the page titled "Weather". This page also serves as the default that the user is sent to upon every subsequent login. The security code popup that displayed after sign up will not show again unless signing up with another account, but the information it displayed can be found in the 'My Account' section. 

The weather app page provides a simple UI for the user to input a city, state, country, or other generally accepted location formats to find out the current weather. Upon entering a location and clicking the check weather button, a closeable container will pop up, describing the inputted location's current weather at the time of entry. The information present is derived from a weather api (api.openweathermap.org), and displays the location entered, weather forecast, temperature (F) and small description of the forecast, as well as a small icon that shows an image of the projected forecast. 

Learning how to implement the API was not trivial for my first time doing so for a project, but once I figured out how, it seemed simple enough. I also learned how to apply a background-color in the form of a gradient using CSS, to design the weather forecast display to have a sky-like color. 

## Nav Bar
The top right of the navigation bar on top of each page changes who it is welcoming based on the username of the user's account. It also acts as a drop down menu that displays each of the pages accesible on this web app. Each section in the drop down list increases in size scale, as well as opacity value when hovered over, to enhance UX and ease of seeing which web page is being selected.

The center of the nav bar is a simple header that changes based on which page the user is currently on. The top left of the nav bar displays 2-DUE in the logo colors, inspired by Google, that acts as a link to send the user back to the initial page's state when first loaded. 

## 2-DUE Daily
This is the main to-do list page of this app. It consists of three forms that allow the user to manipulate goals and activities they want to add to their schedule. The first form at the top is used to set the goal, decide on a frequency, and submit to the list of goals. The frequency is a selection choice of either "today" or "everyday". Depending on how often the user wants to do this action, the goal written in the text field will be sent to the appropriate table of goals. 

The second form consists of two tables - one for the date chosen's tasks and one for everyday tasks - as well as a date input field that the user can change and manipulate as they see fit. One may want to change the date to the past to view their history or consistency in certain areas. The date field allows them to change the goals they are currently viewing. Next to each task/goal on the table, there is a "complete" column with checkboxes next to each task. The user can check the checkbox and hit the "save changes" button to save all completed tasks. The reverse is also true if the user finds they did not actually complete a task they might've thought to before. 

Lastly, at the very bottom of the page is a form used to remove tasks completely from their table. Each task is given a unique id# that is displayed to the left of each task seen in the tables. Entering the id# into the removal form and hitting the "remove task" button will remove the task from whichever table it is found in, as well as the user's database entry for that goal in the backend. 

## 2-DUE Monthly/Yearly
The monthly and yearly sections for this app were made using the 2-DUE Daily page as a template with minor adjustments to the HTML text to imply whether it is monthly or yearly. The same rules apply to both of these pages as the Daily page. The only difference is how it is saved in the server-side of the application, saving with different frequencies in the database to be able to differentiate which page certain goals should go into. 

## My Account
The "My Account" page features the user that is logged in's username and security code, as well as three buttons to modify the user's account info. The change username is simple and allows the user to modify the username, as long as it falls within the textlength criteria and is not taken already. The change password follows a similar layout and allows the user to change their password. There is a show password checkbox available for the user as they see fit, as well as a confirm password field for greater UX. Finally, there is a delete account button that removes the user's information from the database, preventing future log on attempts and deleting all the user's goal history from ever being accessed again. 

## Logout
The logout page is simple, logs the user out, clears the session/cookie, and redirects the user to the first login/welcome page that the user sees when trying to sign up/login. 