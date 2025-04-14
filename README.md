# 🖥️ Application Status Monitor

A web-based monitoring dashboard built with **Flask**, **MySQL**, and **JavaScript**. This tool allows developers and operations teams to monitor the status and response time of application endpoints in real-time.

---

## 📦 Features

- 🔗 Add endpoints (URLs) for monitoring
- 🎯 Auto status check with color-coded indicators:
  - 🟢 Green: Fast (under 1000ms)
  - 🟡 Amber: Slow (above 1000ms)
  - 🔴 Red: Down/unreachable
  - ⚪ Grey: No data
- 🔄 Start/Stop monitoring with interval polling
- ⌚ View real-time response times (ms)
- 🗑️ Delete individual or all entries
- 🛢️ MySQL DB integration via SQLAlchemy

---

## ⚙️ Tech Stack

- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Backend**: Python 3, Flask, SQLAlchemy
- **Database**: MySQL 5.7+ or MySQL 8+
- **Tools**: AJAX, Fetch API

---
## 📁 File Structure
.
├── templates/
│   └── index.html       # Main HTML page
├── app.py               # Flask backend
├── requirements.txt     # Dependencies
└── README.md            # Project documentation

---
##  Install Dependencies
pip install -r requirements.txt

---
## MySQL Database Setup
CREATE DATABASE endpoint;

CREATE TABLE Tb2_ResponseTime (
    Response_id INT AUTO_INCREMENT PRIMARY KEY,
    shortName VARCHAR(100),
    url VARCHAR(1000),
    interval_time_second INT,
    status BIT DEFAULT 0,
    created_date DATETIME
);

---
## Configure DB Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@localhost/endpoint'

---
## Run the Flask App
python app.py

---
## Then visit in your browser:
http://127.0.0.1:5000

---
## 🌐 API Endpoints
Method	Endpoint	Description
GET	/	Load dashboard UI
POST	/add	Add new app URL for monitoring
DELETE	/delete/<id>	Delete a specific record
GET	/get	Retrieve all monitored apps
GET	/status/<id>	Get status and response time
DELETE	/clear	Delete all entries
