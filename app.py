import mysql.connector
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
db = mysql.connector.connect(
    host="localhost",
    user="sravanthi",
    password="12345",
    database="smart_job_portal"
)

cursor = db.cursor()
print("connected to MYSQL successfully!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT COUNT(*) FROM applied_jobs")
            applied = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM saved_jobs")
            saved = cursor.fetchone()[0]

            total = 10

            return render_template(
                "dashboard.html",
                 name=user[1],
                 total=total,
                 applied=applied,
                 saved=saved
            )
        else:
            return "Invalid Email or Password!"

    return render_template("login.html")

@app.route("/register")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute(
    "INSERT INTO users(fullname, email, password) VALUES (%s, %s, %s)",
    (name, email, password)
)
        db.commit()

        return f"Welcome {name}! Registration Successful."

    return render_template("register.html")
@app.route("/search_jobs")
def search_jobs():

    keyword = request.args.get("keyword", "").lower()
    category = request.args.get("category", "")
    jobs = [
    {"title": "Python Developer", "company": "TCS", "location": "Hyderabad"},
    {"title": "DevOps Engineer", "company": "Infosys", "location": "Bengaluru"},
    {"title": "Cloud Engineer", "company": "Wipro", "location": "Chennai"},
    {"title": "Java Developer", "company": "Accenture", "location": "Pune"},
    {"title": "Frontend Developer", "company": "Cognizant", "location": "Hyderabad"},
    {"title": "Backend Developer", "company": "Capgemini", "location": "Bengaluru"},
    {"title": "AWS Cloud Engineer", "company": "IBM", "location": "Mumbai"},
    {"title": "Linux Administrator", "company": "HCL", "location": "Noida"},
    {"title": "Site Reliability Engineer", "company": "Oracle", "location": "Hyderabad"},
    {"title": "Software Engineer", "company": "Tech Mahindra", "location": "Chennai"}
    ]
    if keyword:
        filtered_jobs = []

        for job in jobs:
            if (
               (keyword in job["title"].lower() or keyword in job["company"].lower())
        and
               (category == "" or job["category"] == category)
    ):
                filtered_jobs.append(job)
    else:
        filtered_jobs = jobs
    return render_template("search_jobs.html",jobs=filtered_jobs)    
@app.route("/apply", methods=["POST"])
def apply():
    job_title = request.form["job_title"]
    company = request.form["company"]

    cursor.execute(
        "SELECT * FROM applied_jobs WHERE job_title=%s AND company=%s",
        (job_title, company)
    )

    existing_job = cursor.fetchone()

    if existing_job:
        return "You have already applied for this job."

    cursor.execute(
        "INSERT INTO applied_jobs (job_title, company) VALUES (%s, %s)",
        (job_title, company)
    )

    db.commit()

    return f"You have successfully applied for {job_title} at {company}!"
@app.route("/applied_jobs")
def applied_jobs():

    cursor.execute("SELECT * FROM applied_jobs")

    jobs = cursor.fetchall()

    return render_template("applied_jobs.html", jobs=jobs)
@app.route("/profile")
def profile():

    cursor.execute("SELECT * FROM users LIMIT 1")

    user = cursor.fetchone()

    return render_template("profile.html", user=user)
@app.route("/logout")
def logout():
    return redirect("/login")
@app.route("/upload_resume")
def upload_resume():
    return render_template("upload_resume.html")


@app.route("/upload_resume", methods=["POST"])
def upload_resume_post():
    resume = request.files["resume"]

    if resume:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
        resume.save(filepath)
        return "Resume uploaded successfully!"

    return "No file selected."
@app.route("/save_job", methods=["POST"])
def save_job():
    job_title = request.form["job_title"]
    company = request.form["company"]

    cursor.execute(
        "SELECT * FROM saved_jobs WHERE job_title=%s AND company=%s",
        (job_title, company)
    )

    existing_job = cursor.fetchone()

    if existing_job:
        return "You have already saved this job."

    cursor.execute(
        "INSERT INTO saved_jobs (job_title, company) VALUES (%s, %s)",
        (job_title, company)
    )

    db.commit()

    return "Job saved successfully!"
@app.route("/saved_jobs")
def saved_jobs():

    cursor.execute("SELECT * FROM saved_jobs")
    jobs = cursor.fetchall()

    return render_template("saved_jobs.html", jobs=jobs)
@app.route("/delete_saved_job", methods=["POST"])
def delete_saved_job():
    job_title = request.form["job_title"]
    company = request.form["company"]

    cursor.execute(
        "DELETE FROM saved_jobs WHERE job_title=%s AND company=%s",
        (job_title, company)
    )
    db.commit()

    return redirect("/saved_jobs")
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        cursor.execute(
            "UPDATE users SET fullname=%s, email=%s LIMIT 1",
            (name, email)
        )
        db.commit()

        return redirect("/profile")

    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()

    return render_template("edit_profile.html", user=user)
@app.route("/job/<int:job_id>")
def job_details(job_id):

    jobs = [
        {
            "title": "Python Developer",
            "company": "TCS",
            "category":"Software Development",
            "location": "Hyderabad",
            "experience": "0-2 Years",
            "salary": "₹4-6 LPA",
            "skills": "Python, Flask, MySQL, Git",
            "description": "Looking for a Python Developer with Flask knowledge."
        },
        {
            "title": "DevOps Engineer",
            "company": "Infosys",
            "category":"DevOps",
            "location": "Bengaluru",
            "experience": "1-3 Years",
            "salary": "₹5-8 LPA",
            "skills": "Linux, Docker, Kubernetes, Jenkins",
            "description": "Maintain CI/CD pipelines and cloud infrastructure."
        },
        {
            "title": "Cloud Engineer",
            "company": "Wipro",
            "category":"Cloud Computing",
            "location": "Chennai",
            "experience": "0-2 Years",
            "salary": "₹4-7 LPA",
            "skills": "AWS, EC2, S3, IAM",
            "description": "Manage and deploy cloud applications."
        },
        {
    "title": "Java Developer",
    "company": "Accenture",
    "category":"Software Development",
    "location": "Hyderabad",
    "experience": "1-3 Years",
    "salary": "₹5-8 LPA",
    "skills": "Java, Spring Boot, MySQL",
    "description": "Develop and maintain Java-based web applications."
        },
        {
    "title": "Frontend Developer",
    "company": "Cognizant",
    "category":"Software Development",
    "location": "Pune",
    "experience": "0-2 Years",
    "salary": "₹4-6 LPA",
    "skills": "HTML, CSS, JavaScript, React",
    "description": "Build responsive and user-friendly web interfaces."
        },
        {
    "title": "Backend Developer",
    "company": "Capgemini",
    "category":"Software Development",
    "location": "Bengaluru",
    "experience": "1-3 Years",
    "salary": "₹5-7 LPA",
    "skills": "Python, Flask, MySQL",
    "description": "Develop backend APIs and manage databases."
        },
        {
    "title": "AWS Cloud Engineer",
    "company": "IBM",
    "category":"Cloud Computing",
    "location": "Mumbai",
    "experience": "1-2 Years",
    "salary": "₹6-9 LPA",
    "skills": "AWS, EC2, S3, IAM",
    "description": "Deploy and manage cloud infrastructure on AWS."
        },
        {
    "title": "Linux Administrator",
    "company": "HCL",
    "category":"DevOps",
    "location": "Noida",
    "experience": "1-3 Years",
    "salary": "₹4-7 LPA",
    "skills": "Linux, Bash, Shell Scripting",
    "description": "Manage Linux servers and troubleshoot system issues."
        },
        {
    "title": "Site Reliability Engineer",
    "company": "Oracle",
    "category":"Devops",
    "location": "Hyderabad",
    "experience": "2-4 Years",
    "salary": "₹8-12 LPA",
    "skills": "Docker, Kubernetes, Monitoring",
    "description": "Ensure reliability and scalability of production systems."
        },
        {
    "title": "Software Engineer",
    "company": "Tech Mahindra",
    "category":"Software Development",
    "location": "Chennai",
    "experience": "0-2 Years",
    "salary": "₹4-6 LPA",
    "skills": "Python, Java, SQL",
    "description": "Design, develop, test, and maintain software applications."
}
    ]

    return render_template("job_details.html", job=jobs[job_id])
@app.route("/admin")
def admin():
    return render_template(
        "admin_dashboard.html"
    )
            
if __name__ == "__main__":
    app.run(debug=True)



