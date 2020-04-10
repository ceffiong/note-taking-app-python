# note-taking-app-python
This repo contains source codes for a note-taking application developed in Python. The tutorial can be find here: https://medium.com/@ceffiong/build-a-note-taking-app-with-mysql-backend-in-python-927b4c5fad91?sk=a57e187ba5d8275d8fef32670f9f461d and A demo of the running app can be seen here: https://youtu.be/qWHAvUGb8d4


To start the app:

1) Ensure you have Python installed/setup on your computer - https://www.python.org/downloads/
2) Ensure you have installed/setup Tkinter library (for GUI) - see https://tkdocs.com/tutorial/install.html
3) Ensure you have install/setup a mysql server. For example XAMPP - https://www.apachefriends.org/download.html
4) Open the file "note_app.py" and change the database config to match yours e.g. 

```
# DATABASE FUNCTIONS STARTS
conn = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  passwd=""
)

```

5) If you go through step 4 then just do: "python note_app.py" in your cmd prompt or (run from your choiced IDE) to run the application
6) Good luck!


