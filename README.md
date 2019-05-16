# Open Trivia Quiz

This dynamic web application hosts trivia quiz games, that allows for the creation and participation of tournaments. Developed using Django, MySQL and the Open Trivia Database RESTful API. Includes robust functionality, MVC architecture and automated testing.

An admin user is able to create tournaments with basic information such as name, start and end dates, advanced settings include various categories and difficulties to select from. When a user logs in, they are displayed a list of active and upcoming tournaments in which they can participate. Their scores are recorded and displayed at the end. Additionally, displays a list of users with high scores for past tournaments.

## Getting Started

<ul>
    <li>Pull down the repo</li>
    <li>Download python, this will include pip to allow you to download packages</li>
    <li>Open command prompt and navigate to the mysite folder</li>
    <li>Run python manage.py runserver, leave this running in the background</li>
    <li>Open an internet browser and navigate to http://localhost:8080/</li>
</ul>

## Prerequisites

<ul>
    <li>Download a python editor</li>
    <li>Download all required packages found in requirements.txt using pip</li>
</ul>


```
Python editor example: PyCharm

```

## Installing

### App Server

1. Download a python editor
```
Recommended editor: PyCharm
```
2. Pull the repo
```
https://github.com/fawazd/Open-Trivia-Quiz.git
```
3. Open mysite/manage.py in PyCharm
4. Click 'Configure Python Interpreter' in the top right of the window
```
Will be in a yellow alert bar that will drop down
```
5. In the top right of the new window click the cog then 'Add Local...'
6. Check New environment and choose a location for the virtual environment
7. Change the base interpreter to be python 3.6 or higher
```
If using polytechnic computers select the option 'C:\Program Files(x86)\Python36-32\python.exe'
```
8. Check 'Inherit global site-packages' and press ok
9. You will now have a virtual environment named venv
10. Open command prompt and navigate to it
```
Any command shell will work like powershell
```
11. Inside venv run '.\Scripts\activate'
```
You should now be running in your environment you will have (venv) before your command prompt
```
12. Now navigate to the repo
13. Run the command `pip install -r requirements.txt` this will download all the packages needed
14. Now navigate into the vda folder, there should be a file called manage.py in here
15. Run the command python manage.py runserver
```
Keep this running in the background
```
16. Now open an internet browser and navigate to http://localhost:8080
```
Congrats you have opened the project
```

## Built With

* [Python](https://docs.python.org/3/) - The language used
* [MySQL](https://dev.mysql.com/doc/) - Database
* [Django](https://docs.djangoproject.com/en/2.1/) - The project was built in


## Versioning

- mysqlclientrequests
- Django==2.0.3
- pytz==2018.3


## Authors
 
* **Fawaz Khan Dinnunhan**
