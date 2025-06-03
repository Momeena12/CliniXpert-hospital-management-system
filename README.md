# CliniXpert Hospital Management System 

<img width="1512" alt="Screenshot 2025-06-03 at 8 11 32 PM" src="https://github.com/user-attachments/assets/42639f1b-d865-4798-85d1-a3d2d6ed93d5" />


## Overview

The CliniXpert (Hospital Management System) is a web application designed to facilitate the management of hospital operations, including patient registration, doctor management, appointment scheduling, and administrative tasks. Built using Flask and MySQL, this application provides a user-friendly interface for both administrators and patients.

## Features

- **Admin Features:**
  - Admin login and dashboard
  - Manage patients (view, edit, delete)
  - Manage doctors (view, add, delete)
  - Manage appointments (view, update status)
  
- **User  Features:**
  - User registration and login
  - View and manage personal appointments
  - Book new appointments with doctors

<img width="1512" alt="Screenshot 2025-06-03 at 8 15 32 PM" src="https://github.com/user-attachments/assets/0a034392-5898-44b8-9bbc-a851f6d70027" />

<img width="1510" alt="Screenshot 2025-06-03 at 8 14 42 PM" src="https://github.com/user-attachments/assets/1f36cdd6-9ccf-4b42-806e-04f1ea54b020" />


## Technologies Used

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS
- **Libraries:** Flask, mysql-connector-python

## Installation
- Python 
- MySQL Server
- pip (Python package installer)

### Steps to Set Up

1. **Clone the Repository:**
   bash
   git clone https://github.com/Momeena12/hospital-management-system.git
   cd hospital-management-system
   

2. **Create a Virtual Environment:**
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   

3. **Install Required Packages:**
   bash
   pip install -r requirements.txt
   

4. **Set Up the Database:**
   - Create a new database in MySQL:
     sql
     CREATE DATABASE HMSystem;
     
   - Run the SQL scripts provided in `MYSQLsqlconnector.session.sql` to create tables and insert sample data.

5. **Configure Database Connection:**
   - Update the `config.py` file with your MySQL credentials:
     python
     db_config = {
         'host': 'localhost',
         'port': 3306,
         'user': 'your_username',
         'password': 'your_password',
         'database': 'HMSystem'
     }
    

6. **Run the Application:**
   bash
   python app.py
   - Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage
- **Admin Login:** Access the admin dashboard to manage patients, doctors, and appointments.
- **User  Registration:** New users can register and log in to book and manage their appointments.

## File Structure
hospital-management-system/
Here’s the file structure formatted as a bullet list for your GitHub README:

- **hospital-management-system/**
  - `app.py`                     - Main application file
  - `config.py`                  - Database configuration
  - `requirements.txt`           - Python dependencies
  - `MYSQLsqlconnector.session.sql` - SQL scripts for database setup
  - **templates/**                 - HTML templates
    - `add_doctor.html`
    - `admin_dashboard.html`
    - `admin_doctors.html`
    - `admin_patients.html`
    - `admin_appointments.html`
    - `book_appointment.html`
    - `edit_patient.html`
    - `home.html`
    - `login_admin.html`
    - `login_user.html`
    - `register_user.html`
    - `user_appointments.html`
    - `user_dashboard.html`
  - **static/**                   - Static files (CSS, images)
    - `style.css`
    - **images/**

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## Acknowledgments
- Thanks to the Flask community for their support and documentation.
- Special thanks to the contributors who helped improve this project.

For any Queries reach out to us at momeenaa03@gmail.com
LinkeDin: https://www.linkedin.com/in/momeena-azhar-0b9943288?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app
