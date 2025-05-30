from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'HMSystem'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Database error: {e}")
        return None

# --- All existing routes from previous responses remain here ---
# home, admin_login, user_register, user_login, admin_dashboard, user_dashboard, logout
# view_patients, edit_patient, delete_patient
# view_doctors, add_doctor, delete_doctor
# view_appointments_user, book_appointment
# --- We will add the new appointment status update route and modify view_appointments (admin) ---


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        if not conn: flash("Database connection error.", "error"); return render_template('login_admin.html', error="Database connection error.")
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
            admin = cursor.fetchone()
        except Error as e: flash(f"Error during login: {e}", "error"); admin = None
        finally: cursor.close(); conn.close()
        if admin:
            session['admin_logged_in'] = True; session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else: return render_template('login_admin.html', error="Invalid credentials.")
    return render_template('login_admin.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']; email = request.form['email']; password = request.form['password']
        age_str = request.form.get('age'); gender = request.form.get('gender')
        age = int(age_str) if age_str and age_str.isdigit() else None
        if gender == "": gender = None
        conn = get_db_connection()
        if not conn: flash("Database connection error.", "error"); return render_template('register_user.html', error="DB error.",name=name, email=email, age=age_str, gender=gender)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM patients WHERE email = %s", (email,))
            if cursor.fetchone(): flash("Email already registered.", "error"); return render_template('register_user.html', error="Email exists.", name=name, age=age_str, gender=gender, email=email)
            cursor.execute("INSERT INTO patients (name, email, password, age, gender) VALUES (%s, %s, %s, %s, %s)", (name, email, password, age, gender))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('user_login'))
        except Error as e: conn.rollback(); flash(f"An error occurred: {e}", "error"); return render_template('register_user.html', error=str(e), name=name, email=email, age=age_str, gender=gender)
        finally: cursor.close(); conn.close()
    return render_template('register_user.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']; password = request.form['password']
        conn = get_db_connection()
        if not conn: flash("Database connection error.", "error"); return render_template('login_user.html', error="DB error.")
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM patients WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
        except Error as e: flash(f"Login error: {e}", "error"); user = None
        finally: cursor.close(); conn.close()
        if user:
            session['user_logged_in'] = True; session['user_email'] = email; session['user_name'] = user['name']
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid email or password, or email not registered.", "error")
            return render_template('login_user.html', error="Invalid credentials or email not registered.")
    return render_template('login_user.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    if not session.get('user_logged_in'): return redirect(url_for('user_login'))
    return render_template('user_dashboard.html', user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.clear(); flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/admin/patients')
def view_patients():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn: flash("Database connection error.", "error"); return render_template('admin_patients.html', patients=[])
    cursor = conn.cursor(dictionary=True)
    patients = []
    try:
        cursor.execute("SELECT id, name, email, age, gender, phone, address FROM patients")
        patients = cursor.fetchall()
    except Error as e: flash(f"Error fetching patients: {e}", "error")
    finally: cursor.close(); conn.close()
    return render_template('admin_patients.html', patients=patients)

@app.route('/admin/patient/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn: flash("DB error.", "error"); return redirect(url_for('view_patients'))
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']; email = request.form['email']
        age_str = request.form.get('age'); gender = request.form.get('gender')
        phone = request.form.get('phone'); address = request.form.get('address')
        age = int(age_str) if age_str and age_str.isdigit() else None
        if gender == "": gender = None
        try:
            cursor.execute("SELECT id FROM patients WHERE email = %s AND id != %s", (email, patient_id))
            if cursor.fetchone():
                flash("Email already in use by another patient.", "error")
                cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                patient_data = cursor.fetchone()
                return render_template('edit_patient.html', patient=patient_data, error="Email already in use.")
            sql = "UPDATE patients SET name=%s, email=%s, age=%s, gender=%s, phone=%s, address=%s WHERE id=%s"
            cursor.execute(sql, (name, email, age, gender, phone, address, patient_id))
            conn.commit(); flash("Patient details updated.", "success")
            return redirect(url_for('view_patients'))
        except Error as e:
            conn.rollback(); flash(f"Error updating patient: {e}", "error")
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,)) # Re-fetch for form
            patient_data = cursor.fetchone()
            return render_template('edit_patient.html', patient=patient_data, error=str(e))
        finally: cursor.close(); conn.close() 
    else: # GET request
        try:
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cursor.fetchone()
            if not patient: flash("Patient not found.", "error"); return redirect(url_for('view_patients'))
            return render_template('edit_patient.html', patient=patient)
        except Error as e: flash(f"Error fetching patient: {e}", "error"); return redirect(url_for('view_patients'))
        finally: cursor.close(); conn.close() 

@app.route('/admin/patient/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn: flash("DB error.", "error"); return redirect(url_for('view_patients'))
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        if cursor.rowcount > 0: flash("Patient deleted.", "success")
        else: flash("Patient not found.", "warning")
    except Error as e: conn.rollback(); flash(f"Error deleting patient: {e}", "error")
    finally: cursor.close(); conn.close()
    return redirect(url_for('view_patients'))

@app.route('/admin/doctors')
def view_doctors():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn: flash("Database connection error.", "error"); return render_template('admin_doctors.html', doctors=[])
    cursor = conn.cursor(dictionary=True)
    doctors = []
    try: 
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
    except Error as e: flash(f"Error fetching doctors: {e}", "error")
    finally: cursor.close(); conn.close()
    return render_template('admin_doctors.html', doctors=doctors)

@app.route('/admin/doctor/add', methods=['GET', 'POST'])
def add_doctor():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']; email = request.form['email']
        specialty = request.form.get('specialty'); phone = request.form.get('phone')
        if not name or not email:
            flash("Name and Email are required.", "error")
            return render_template('add_doctor.html', error="Name and Email are required.", name=name, email=email, specialty=specialty, phone=phone)
        conn = get_db_connection()
        if not conn: flash("DB error.", "error"); return render_template('add_doctor.html', error="Database error.", name=name, email=email, specialty=specialty, phone=phone)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM doctors WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email already exists for a doctor.", "error")
                return render_template('add_doctor.html', error="Email exists.", name=name, email=email, specialty=specialty, phone=phone)
            sql = "INSERT INTO doctors (name, email, specialty, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, specialty if specialty else None, phone if phone else None))
            conn.commit(); flash("Doctor added successfully.", "success")
            return redirect(url_for('view_doctors'))
        except Error as e:
            conn.rollback(); flash(f"Error adding doctor: {e}", "error")
            return render_template('add_doctor.html', error=str(e), name=name, email=email, specialty=specialty, phone=phone)
        finally: cursor.close(); conn.close()
    return render_template('add_doctor.html')

@app.route('/admin/doctor/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn: flash("DB error.", "error"); return redirect(url_for('view_doctors'))
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
        conn.commit()
        if cursor.rowcount > 0: flash("Doctor deleted.", "success")
        else: flash("Doctor not found.", "warning")
    except Error as e:
        conn.rollback()
        if e.errno == 1451: flash(f"Cannot delete doctor. Still referenced in other records (e.g. appointments not cascaded). Error: {e}", "error")
        else: flash(f"Error deleting doctor: {e}", "error")
    finally: cursor.close(); conn.close()
    return redirect(url_for('view_doctors'))

@app.route('/admin/appointments') # This is the existing route for viewing appointments
def view_appointments():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "error")
        return render_template('admin_appointments.html', appointments=[])
    cursor = conn.cursor(dictionary=True)
    appointments = []
    try:
        # Ensure the status column is selected
        cursor.execute("""
            SELECT a.id, a.appointment_date, a.time_slot, a.status, 
                   p.name AS patient_name, d.name AS doctor_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date DESC, a.time_slot ASC 
        """) # Added ORDER BY for better viewing
        appointments = cursor.fetchall()
    except Error as e:
        flash(f"Error fetching appointments: {e}", "error")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return render_template('admin_appointments.html', appointments=appointments)

# --- NEW: Update Appointment Status Route ---
@app.route('/admin/appointment/update_status/<int:appointment_id>/<string:new_status>', methods=['POST'])
def update_appointment_status(appointment_id, new_status):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    valid_statuses = ['Conducted', 'Cancelled', 'Scheduled'] # Add 'Scheduled' for re-scheduling
    if new_status not in valid_statuses:
        flash("Invalid status update.", "error")
        return redirect(url_for('view_appointments'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "error")
        return redirect(url_for('view_appointments'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE appointments SET status = %s WHERE id = %s", (new_status, appointment_id))
        conn.commit()
        if cursor.rowcount > 0:
            flash(f"Appointment status updated to '{new_status}'.", "success")
        else:
            flash("Appointment not found or status already updated.", "warning")
    except Error as e:
        conn.rollback()
        flash(f"Error updating appointment status: {e}", "error")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    return redirect(url_for('view_appointments'))


@app.route('/user/appointments')
def view_appointments_user():
    if not session.get('user_logged_in'): return redirect(url_for('user_login'))
    user_email = session.get('user_email')
    conn = get_db_connection()
    if not conn: flash("Database error.", "error"); return render_template('user_appointments.html', appointments=[])
    cursor = conn.cursor(dictionary=True)
    appointments = []
    try:
        cursor.execute("SELECT id FROM patients WHERE email=%s", (user_email,))
        patient = cursor.fetchone()
        if patient:
            # Also fetch status for user's view
            cursor.execute("""
                SELECT a.id, a.appointment_date, a.time_slot, a.status, d.name AS doctor_name 
                FROM appointments a 
                JOIN doctors d ON a.doctor_id = d.id 
                WHERE a.patient_id = %s 
                ORDER BY a.appointment_date DESC, a.time_slot ASC
            """, (patient['id'],))
            appointments = cursor.fetchall()
        else: flash("Patient record not found.", "error")
    except Error as e: flash(f"Error fetching appointments: {e}", "error")
    finally: cursor.close(); conn.close()
    return render_template('user_appointments.html', appointments=appointments)

@app.route('/user/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    if not session.get('user_logged_in'): return redirect(url_for('user_login'))
    if request.method == 'POST':
        conn_post = get_db_connection()
        if not conn_post: flash("DB error.", "error");
        else:
            cursor_post = conn_post.cursor(dictionary=True)
            try:
                date_val = request.form['date']; selected_time_slot = request.form['time_slot']
                doctor_id_val = request.form['doctor_id']; user_email = session.get('user_email')
                cursor_post.execute("SELECT id FROM patients WHERE email=%s", (user_email,))
                patient = cursor_post.fetchone()
                if patient:
                    # Default status is 'Scheduled' by DB schema, but can be explicit
                    sql_insert = "INSERT INTO appointments (appointment_date, time_slot, doctor_id, patient_id, status) VALUES (%s, %s, %s, %s, %s)"
                    insert_values = (date_val, selected_time_slot, doctor_id_val, patient['id'], 'Scheduled')
                    cursor_post.execute(sql_insert, insert_values); conn_post.commit()
                    flash("Appointment booked successfully.", "success")
                    if cursor_post: cursor_post.close()
                    if conn_post: conn_post.close()
                    return redirect(url_for('view_appointments_user'))
                else: flash("Patient record not found.", "error")
            except Error as e:
                if conn_post: conn_post.rollback()
                flash(f"Error booking appointment: {e}", "error")
            finally: 
                if 'cursor_post' in locals() and cursor_post and not cursor_post.is_closed(): cursor_post.close()
                if conn_post and conn_post.is_connected(): conn_post.close()
        doctors_list = []
        conn_doc_fetch = get_db_connection()
        if conn_doc_fetch:
            cursor_doc_fetch = conn_doc_fetch.cursor(dictionary=True)
            try: cursor_doc_fetch.execute("SELECT id, name, specialty FROM doctors"); doctors_list = cursor_doc_fetch.fetchall()
            except Error as e_doc: flash(f"Error fetching doctors: {e_doc}", "error")
            finally: 
                if cursor_doc_fetch: cursor_doc_fetch.close()
                if conn_doc_fetch: conn_doc_fetch.close()
        return render_template('book_appointment.html', doctors=doctors_list)

    doctors = []
    conn_get = get_db_connection()
    if not conn_get: flash("DB error.", "error")
    else:
        cursor_get = conn_get.cursor(dictionary=True)
        try: cursor_get.execute("SELECT id, name, specialty FROM doctors"); doctors = cursor_get.fetchall()
        except Error as e: flash(f"Error fetching doctors: {e}", "error")
        finally: 
            if cursor_get: cursor_get.close()
            if conn_get: conn_get.close()
    return render_template('book_appointment.html', doctors=doctors)


if __name__ == '__main__':
    app.run(debug=True)