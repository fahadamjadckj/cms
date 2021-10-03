# YOUR PROJECT TITLE
#### Video Demo:  <https://youtu.be/h11Hxefk2Ks>
#### Description: CMS is a class management system that is light yet useful in the sense of automating a tedious task of managing students and separate classes while also solving some other problems on the way. Here are some specifications of CMS.
## Technologies used: python, flask, html, css, sqlite3.
## THE LIST OF ALL ROUTES IN app.py:
1. "/"
2. "/login"
3. "/logout"
4. "/register"
5. "/attendance"
6. "/csv"
7. "/notice"
8. "/admin"
9. "/addnotice"
10. "/logoutadmin"
11. "/addclass"
12. "/admincsv"
13. "/about"
**Here is the explanation of each of the routes**

## "/" route:
 **The "/" route is the default route when a user tries to access the website. If the user is registered already he or she can login and will be taken to the "Home" page of the webapp which is specific to each user. If a session doesnt exist for the person trying to access the homepage, it redirects them to */login* route. If the user logs then and only then he is allowed to access the homepage.**

## "/login" route:
**The login route is the first thing presented to the user if the user's session has expired or the user hasn't registered. The login route takes inputs from "login.html" page which are "username" and "password" and compares them in the user's database if a user exists by this name. It compares their username which is "registeration number" in database and their password hash. If the username or password doesn't match any in the database *"userd.db"* it flashes the message *Incorrect username or password"* if the user exists, he or she is directed to the homepage and a session is created by their username so that the user doesnt need to login again and again , untill the session is alive. It also checks if the user has left any inut fields empty.**

## "/register" route:
**Register route is used for adding new students. It takes user inputs from a form in *register.html" which includes name, class and other info, the failure of missing any of the input fields will result in an error and the user will be redirected to the register page again and message is flashed *Incomplete input*. Provided the inputs are complete the user is redirected to the "login" page to login and all that information is INSERTED into the the users.db. It also makes sure that multiple users are not created with the same username and alerts if someone tries to do so.**

## "/attendance" route: The attendance route is used to update the logged in student's attendance for a particular class. The attendance in inserted into the *attendance* table in the *users.db" database.

## "/csv" route:
**The csv route when called, gets all the student attendances from the attendance table in users.db and and calls a function to create a csv file of the record in the static directory. Each file is created with the user's name who is logged in hence when multiple people are logged in they dont endup downloading same or eachothers's files. After generating the csv file in static folder it calls the *url_for* function that creates and url for the file from where the user can download it.**

## "/notice" route:
**The notice route is one of the most important features of this app, it fetches the notices from the notice table in users.db databse and displays them in a table categorized by time, date , summary of the notice and link to the source.**

## "/addnotice" route:
**The addnotice route can only be accessed by the admin in the admin panel. Using this the admin can add new notices important to different classes in same categorization as displayed in notice route. It also sends a email to all the class students to which the notice was concerned hence they dont miss critical news and exam date.**

## "/admin" route:
**The admin route is for administrator of the website only. No registered or non registered student can access it because they have separate login pathways. On providing the right username and password it takes the user to the admin panel. The admin can view but cannot use registeration system of students but can view notice board. If the admin tries to access the attendance system only intended for students the site will return server error. On the admin panel the admin can add new classes to the CMS , add notices, and download the attendance of the whole classes.**
**If the credentials are right the admin logs in and a session is ceated by name "admin" and the admin remains logged in untill the session expires.**
*The default username and passwords of admin page are: "admin" and "satoshi"* **can be changed in the /admin route**.

## "/logout" route:
**The logout route when called clears the session of the currently logged in student and redirects them to the login page.**

## "/logoutadmin" route:
**The logout admin route when called clears the session of admin and redirects to the login page. They have separate logout routes hence the admins or students dont accidently logout eachother of their accounts.**

# Database specs:
**The database used for this project is sqlite3 and comprieses of 3 tables one is called students which contains the students data that they gave to register themselves including first_name, last_name, registeration number, class and account type. It also  gives each student a primary id automatically. There is a 2nd relational table in the database called attendance which stores the attendance of students categorized by registeration number, class, first_name, last_name and time and date which are automatically added when a student marks the attendance for a particular class. The attendance table also assigns each attendance record a FOREIGN id which references the id in students.**

**The 3rd table is called notice and it contains all the notices published till date by the admin categorized by summary, date, time and links to sources**.

# Design choices:
### 1 : Responsive elements:
*All the tables and elements used in the html files or view of the webapp are responsive as more and more people are using their mobile devices to perform tasks that otherwise would have required a computer to perform. This calls for the need to develop our interfaces such that they are also easier and efficient to use on mobile devices so that the user doesnt feel the need to have a computer ready all the time to perform this small task of marking their attendance or viewing a notice.
CMS ensures that the webapp works flawlessly on all the mobile and desktop devices. For this I used bootstrap elements as well as custom css to make elements keep their position on screen. The use of a responsive navbar also makes sure that the interface is as smooth on the mobile device as on a desktop*.

### 2: Dark theme:
*The website's color theme is dark greyish or some degree of black just because the color black is easier on the eyes as compared to white and on amoled screens it also helps save power.*

### 3: Email notifications:
*While designing the webapp my goal was to make it convienient for the students to get hold of the latest notifications from the university without having to check the university website or noticeboards again and again. And I myself have missed the absence of such tool that could just inform us about them. The email system gives the user the ability to read the notice with just a click and they dont miss any notices thats why I used it.

### 4: Ability to download your attendance:
*Previously and I have noticed it too in schools and in some colleges especially in my area there was no way for the student to know how many classes he attended in the year or semester hence could not calculate his or her attendance percentage which is important to maintain in courses. This tool not only gives the student to mark attendance but also to download and look at their attendance in the whole sem, class and csv allows them to quickly calculate their percentage plus it keeps the data organized.

### 5: Cron job usage:
*The addnotice route uses a cronjob to send bulk emails to class students. I used cronjob because it kept the connection alive after one email was sent instead of sending one then connecting again and again which is much slower.

### 6: HASH passwords:
CMS stores only stores user passwords in hashed form so that if somwhow the data is compromised, your personal info remains safe.

# USAGE requirements:
- The webapp requires two environment variables to work without which the addnotice and email functions will not work:
1. export MAIL_PASSWORD="your password"
2. export MAIL_USERNAME="your email"
Be sure to set them before using the CMS.

- The webapp currently only supports 1 class for the students.
- The admin username = "admin"
- The admin password = "satoshi"

3. The demo classes are predefined in classes list in app.py. You can change it to add your own classes or use the admin page to add your classes, to remove demo classes remove them from the classes list.




