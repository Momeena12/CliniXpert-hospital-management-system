CREATE DATABASE IF NOT EXISTS HMSystem;
USE HMSystem;

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL, -- THIS LINE IS CORRECT
    status VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Insert sample admins
INSERT INTO admins (username, password)
VALUES
    ('admin1', 'adminpass123'),
    ('admin2', 'adminpass456')
ON DUPLICATE KEY UPDATE username=username; -- Avoids error if run multiple times

-- Insert sample patient
INSERT INTO patients (name, email, password, phone, address)
VALUES
    ('John Doe', 'john.doe@example.com', 'john1234', '1234567890', '123 Main Street, City')
ON DUPLICATE KEY UPDATE email=email; -- Avoids error if run multiple times

-- Insert sample doctors
INSERT INTO doctors (name, specialty, phone, email)
VALUES
    ('Dr. Alice Smith', 'Cardiology', '555-0101', 'alice.smith@hospital.com'),
    ('Dr. Bob Johnson', 'Pediatrics', '555-0102', 'bob.johnson@hospital.com'),
    ('Dr. Carol Williams', 'Neurology', '555-0103', 'carol.williams@hospital.com'),
    ('Dr. David Brown', 'Orthopedics', '555-0104', 'david.brown@hospital.com'),
    ('Dr. Emily Jones', 'General Medicine', '555-0105', 'emily.jones@hospital.com')
ON DUPLICATE KEY UPDATE email=email; 




ALTER TABLE patients ADD COLUMN gender VARCHAR(10);

