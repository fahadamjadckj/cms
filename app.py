import os
import re
from flask import Flask, session, redirect, render_template, request, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from cs50 import SQL
from flask_mail import Mail, Message


# configuring application:
app = Flask(__name__)

# ensure that the templates are autoreloaded:
app.config["TEMPLATES_AUTO_RELOAD"] = True 

# configuring session cookies:
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Specifying database:
db = SQL("sqlite:///users.db")

@app.route("/", methods=["GET", "POST"])
def ho():

    # GET..
    if request.method == "GET":
        if not session.get("user_id"):
            return redirect("/login")
        user_class = db.execute("SELECT * FROM students WHERE registeration_number = ?", session["user_id"])

        # Getting users previous attendance in subject:
        prev_attend = db.execute("SELECT * FROM attendance WHERE registeration_number = ? ORDER BY date LIMIT 10", session["user_id"])

        # checking if the user has attendance records or not:
        if len(prev_attend) == 0 and len(user_class) == 0:
            return render_template("Home.html", user_class="None", prev_attend="0")
        if len(prev_attend) == 0:
            return render_template("Home.html", user_class=user_class[0]["class"], prev_attend="0")
        
        return render_template("Home.html", user_class=user_class[0]["class"], prev_attend=prev_attend)
            
# deifinig classes:
classes = ["STAT-401", "ENG-303", "IS-403", "math-701"]
        

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        
        return render_template("login.html")
    
    if request.method == "POST":
        
        # checking if the user exists in the table:
        chk_user = db.execute("SELECT * FROM students WHERE registeration_number = ?", request.form.get("username"))
        if len(chk_user) == 1:
            if check_password_hash(chk_user[0]["password"], request.form.get("password")):
                session["user_id"] = request.form.get("username")
                return redirect("/")
            flash("incorrect username or password")
            return redirect("/login")

        flash("incorrect username or password")
        return redirect("/login")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["user_id"] = None
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("register.html", classes=classes)

    # POST..
    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last name")
        email = request.form.get("email")
        user_class = request.form.get("class")
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=16)
        student = request.form.get("student")

        # error checking for empty fields:
        if not request.form.get("first_name"):
            flash("No firstname")
            return redirect("/register")
        if not request.form.get("last_name"):
            flash("incomplete Form")
            return redirect("/register")
        if not request.form.get("email"):
            flash("incomplete Form")
            return redirect("/register")
        if not request.form.get("username"):
            flash("incomplete Form")
            return redirect("/register")
        if not request.form.get("password"):
            flash("incomplete form")
            return redirect("/register")
        if not request.form.get("class"):
            flash("incomplete Form")
            return redirect("/register")
        if not request.form.get("student"):
            flash("incompl")
            return redirect("/register")
        if request.form.get("class") not in classes:
            flash("class not found")
            return redirect("/register")

        # storing user data in users table:
        db.execute("INSERT INTO students (first_name, last_name, email, class, registeration_number, password) VALUES(?, ?, ?, ?, ?, ?)", first_name, request.form.get("last_name"), email, user_class, username, password)
        
        flash("Registered, Log In now")
        return redirect("/login")
        
@app.route("/policy")
def policy():
    return render_template("policy.html")

@app.route("/attendance", methods=["GET", "POST"])
def attendance():
     if request.method == "POST":

        # checking for empty fields:
        if not request.form.get("first_name"):
            flash("No first_name")
            return redirect("/")
        if not request.form.get("last_name"):
            flash("No last Name")
            return redirect("/")
        if not request.form.get("class"):
            flash("No Class")
            return redirect("/")
        if request.form.get("registeration_number") != session["user_id"]:
            flash("Not your registeration")
            return redirect("/")
        if not request.form.get("registeration_number"):
            flash("No REG number")
            return redirect("/")
        
        # stroing values:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        registeration = request.form.get("registeration_number")
        user_class = request.form.get("class")
        
        # adding to attendance table:
        user = db.execute("SELECT id FROM students WHERE registeration_number = ?", session["user_id"])
        db.execute("INSERT INTO attendance (attend_id, first_name, last_name, registeration_number, class, date, time) VALUES(?, ?, ?, ?, ?, datetime('now'), datetime('localtime'))", user[0]["id"], first_name, last_name, registeration, user_class)

        flash("Attendance Marked!")
        return redirect("/")


@app.route("/csv", methods=["GET", "POST"])
def cf():
    if request.method == "POST":
        name = "static/" + session["user_id"] + ".csv"
        name2 = session["user_id"] + ".csv"
        file = open(name, 'w')

        # creating header:
        print("FIRST NAME, LAST NAME, REG, DATE TIME", file = file)
        
        # getting the records of currently logged in user:
        attend = db.execute("SELECT * FROM attendance WHERE registeration_number = ?", session["user_id"])

        # writing comma separated values:
        for row in attend:
            first = row["first_name"]
            last = row["last_name"]
            reg = row["registeration_number"]
            date = row["date"]
            print(f"{first}, {last}, {reg}, {date}", file = file)

        # closing file:
        file.close()
        url = url_for("static", filename=name2)
        
        # redirecting them to the download link:
        return redirect(url)

# noticeboard route:
@app.route("/notice", methods=["GET", "POST"])
def noticedisplay():
    if request.method == "GET":
        if not session.get("user_id"):
            return redirect("/login")
        
        # retrieving notices from notice table:
        notices = db.execute("SELECT * FROM notice ORDER by issue_date LIMIT 10")
        return render_template("notice.html", notices=notices)

# admin route:
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        if not session.get("admin_id"):
            return render_template("admin_login.html")
        return render_template("admin_panel.html", classes=classes)

    if request.method == "POST":
        if not request.form.get("username"):
            flash("Incorrect username or password")
            return redirect("/admin")
        if not request.form.get("password"):
            flash("Incorrect username or password")
            return redirect("/admin")

        # setting default username and password:
        if request.form.get("username") == "admin" and request.form.get("password") == "satoshi":
            session["admin_id"] = request.form.get("username")
            return render_template("admin_panel.html", classes=classes)
        flash("Incorrect username or password")
        return redirect("/admin")

# adding notice route:
@app.route("/addnotice", methods=["GET", "POST"])
def add_notice():
    
    # error checking:
    if not request.form.get("class"):
        flash("No class selected")
        return redirect("/admin")
    if not request.form.get("issue_date"):
        flash("No issue date")
        return redirect("/admin")
    if not request.form.get("summary"):
        flash("No summary")
        return redirect("/admin")
    # adding notice to notice table in database:
    db.execute("INSERT INTO notice (issue_date, summary, class, link, time) VALUES(?, ?, ?, ?, TIME('now'))", request.form.get("issue_date"), request.form.get("summary"), request.form.get("class"), request.form.get("link"))

     # sending mail to class students:
    app = Flask(__name__)

    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_ASCII_ATTACHMENTS"] = True
    mail = Mail(app)

    # getting their emails:
    emails = db.execute("SELECT * FROM students WHERE class = ?", request.form.get("class"))
    addresses = []
    for email in emails:
        addresses.append(email["email"])

    # Cron-job to send bulk emails;
    # Source: flask documentation. https://pythonhosted.org/Flask-Mail/
    with mail.connect() as conn:
        for address in addresses:
            message = request.form.get("summary")
            subject = "CMS New Noitce"
            msg = Message(sender=os.getenv("MAIL_USERNAME"), recipients=[address],
                      body=message,
                      subject=subject)
            conn.send(msg)
    flash("notice published")
    return redirect("/admin")

# logout route for admin:
@app.route("/logoutadmin", methods=["GET", "POST"])
def logout_admin():
    session["admin_id"] = None
    return redirect("/login")

# adding or removing class route:
@app.route("/addclass", methods=["GET", "POST"])
def add_class():
    if not request.form.get("class_name"):
        flash("No class specified")
        return redirect("/admin")

    # adding class:
    classes.append(request.form.get("class_name"))
    flash("Class Added")
    return redirect("/admin")

# admin csv download route:
@app.route("/admincsv", methods=["GET", "POST"])
def admin_csv():
    
        # error check:
    if not request.form.get("class"):
        flash("No class selected")
        return redirect("/admin")

    name = "static/" + session["admin_id"] + ".csv"
    name2 = session["admin_id"] + ".csv"
    file = open(name, 'w')

    # creating header:
    print("FIRST NAME, LAST NAME, REG, DATE TIME", file = file)
        
    # getting the records of currently logged in user:
    attend = db.execute("SELECT * FROM attendance WHERE class = ?", request.form.get("class"))

    # writing comma separated values:
    for row in attend:
        first = row["first_name"]
        last = row["last_name"]
        reg = row["registeration_number"]
        date = row["date"]
        print(f"{first}, {last}, {reg}, {date}", file = file)

    # closing file:
    file.close()
    url = url_for("static", filename=name2)
        
    # redirecting them to the download link:
    return redirect(url)

# about section:
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")
    
        





    
