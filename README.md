# 🌍 Tourism and Travel Package Management System

A Django-based web application for managing tourism packages, bookings, and travel itineraries.  
This project uses **Django (backend)**, **MySQL (database)**, and will integrate **Bootstrap (frontend)**.

---

## 🧩 Project Setup (For All Contributors)


### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ Create a Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux/Mac

source venv/bin/activate

3️⃣ Install Dependencies

Install required packages:

pip install django mysqlclient python-dotenv


Then generate the requirements.txt file (only once, by any one teammate):

pip freeze > requirements.txt

pip install -r requirements.txt

4️⃣ Create a .env File

Each team member must create their own .env file inside the project root (not committed to GitHub).

Example .env:

SECRET_KEY=django-insecure-xxxxxx
DEBUG=True

DB_NAME=tourism_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306

5️⃣ Configure the Database

Open MySQL and create the database:

CREATE DATABASE tourism_db;


Make sure your .env values match these credentials.

6️⃣ Apply Migrations

Run:

python manage.py makemigrations
python manage.py migrate

7️⃣ Run the Server
python manage.py runserver


Now visit 👉 http://127.0.0.1:8000/

🧠 Current Project Structure
tourism_project/
│
├── tourism_project/        # Main Django configuration folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env                    # Local environment variables (not pushed)
├── .gitignore
├── manage.py
└── README.md

👥 Team Contribution Workflow
🧩 Create a New Branch

Before starting work:

git checkout -b feature/<feature-name>

🧱 Make Changes, Commit, and Push
git add .
git commit -m "Added <short-description>"
git push origin feature/<feature-name>

🔁 Open a Pull Request

Go to GitHub → Open a Pull Request to main → Assign a reviewer.

⚙️ Upcoming Setup Plan

Add static/ directory for Bootstrap assets

Add templates/ directory for HTML files

Create accounts app (authentication system)

Create packages app for managing travel packages

Integrate media uploads for package images

🧾 Notes

Never commit .env or database files.

After pulling updates, always run:

python manage.py makemigrations
python manage.py migrate


Follow PEP 8 code style for Python files.

Use clear and descriptive commit messages.

📦 Tech Stack

Backend: Django

Database: MySQL

Frontend: Bootstrap (to be added)

Version Control: Git & GitHub

Environment Management: Python venv

Added chatbot= visit->   http://127.0.0.1:8000/chatbot to see the chatbot
the app chatbot handles the entire working of the chatbot 
fine tuning is not done so fine_tuning required
