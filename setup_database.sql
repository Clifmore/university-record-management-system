-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    program VARCHAR(50),
    year_of_study INTEGER,
    graduation_status VARCHAR(20)
);

-- Lecturers table
CREATE TABLE IF NOT EXISTS lecturers (
    lecturer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    phone VARCHAR(20),
    office VARCHAR(50)
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    credits INTEGER,
    semester VARCHAR(20),
    lecturer_id VARCHAR(20) REFERENCES lecturers(lecturer_id)
);

-- Course Enrollments table
CREATE TABLE IF NOT EXISTS course_enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id),
    course_id VARCHAR(20) REFERENCES courses(course_id),
    enrollment_date DATE DEFAULT CURRENT_DATE
);

-- Grades table
CREATE TABLE IF NOT EXISTS grades (
    grade_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id),
    course_id VARCHAR(20) REFERENCES courses(course_id),
    grade DECIMAL(5,2),
    semester VARCHAR(20)
);

-- Advisor Assignments table
CREATE TABLE IF NOT EXISTS advisor_assignments (
    assignment_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id),
    lecturer_id VARCHAR(20) REFERENCES lecturers(lecturer_id)
);

-- Research Interests table
CREATE TABLE IF NOT EXISTS research_interests (
    interest_id SERIAL PRIMARY KEY,
    lecturer_id VARCHAR(20) REFERENCES lecturers(lecturer_id),
    research_area VARCHAR(100)
);

-- Insert Students
INSERT INTO students (student_id, name, email, program, year_of_study) VALUES
('S001', 'John Doe', 'john.doe@university.edu', 'Computer Science', 4),
('S002', 'Jane Smith', 'jane.smith@university.edu', 'Engineering', 3),
('S003', 'Bob Johnson', 'bob.johnson@university.edu', 'Computer Science', 4),
('S004', 'Alice Brown', 'alice.brown@university.edu', 'Physics', 2),
('S005', 'Mary Johnson', 'mary.johnson@university.edu', 'Computer Science', 4),
('S006', 'David Wilson', 'david.wilson@university.edu', 'Computer Science', 3);

-- Insert Lecturers
INSERT INTO lecturers (lecturer_id, name, email, department, phone, office) VALUES
('L001', 'Dr. Alan Turing', 'alan.turing@university.edu', 'Computer Science', '555-0101', 'CS 201'),
('L002', 'Dr. Grace Hopper', 'grace.hopper@university.edu', 'Computer Science', '555-0102', 'CS 202'),
('L003', 'Dr. Ada Lovelace', 'ada.lovelace@university.edu', 'Mathematics', '555-0103', 'MATH 101'),
('L004', 'Dr. Jane Smith', 'jane.smith@university.edu', 'Computer Science', '555-0104', 'CS 203');

-- Insert Courses
INSERT INTO courses (course_id, course_code, name, department, credits, semester, lecturer_id) VALUES
('C001', 'CS101', 'Intro to Programming', 'Computer Science', 3, 'Spring 2024', 'L001'),
('C002', 'CS201', 'Data Structures', 'Computer Science', 3, 'Spring 2024', 'L002'),
('C003', 'MATH101', 'Calculus I', 'Mathematics', 3, 'Spring 2024', 'L003'),
('C004', 'CS301', 'Database Systems', 'Computer Science', 3, 'Spring 2024', 'L001'),
('C005', 'CS401', 'Machine Learning', 'Computer Science', 3, 'Spring 2024', 'L004');

-- Insert Enrollments
INSERT INTO course_enrollments (student_id, course_id) VALUES
('S001', 'C001'),
('S003', 'C001'),
('S002', 'C002'),
('S005', 'C003'),
('S001', 'C004'),
('S005', 'C004'),
('S003', 'C005'),
('S006', 'C005'),
('S002', 'C003');

-- Insert Grades
INSERT INTO grades (student_id, course_id, grade, semester) VALUES
('S001', 'C001', 85.5, 'Spring 2024'),
('S003', 'C001', 78.0, 'Spring 2024'),
('S002', 'C002', 92.0, 'Spring 2024'),
('S005', 'C003', 88.0, 'Spring 2024'),
('S001', 'C004', 90.0, 'Spring 2024'),
('S005', 'C004', 95.0, 'Spring 2024'),
('S003', 'C005', 82.0, 'Spring 2024'),
('S006', 'C005', 75.0, 'Spring 2024'),
('S002', 'C003', 79.0, 'Spring 2024'),
('S001', 'C003', 91.0, 'Spring 2024'),
('S003', 'C003', 84.0, 'Spring 2024');

-- Insert Advisor Assignments
INSERT INTO advisor_assignments (student_id, lecturer_id) VALUES
('S001', 'L001'),
('S002', 'L002'),
('S003', 'L001'),
('S005', 'L004'),
('S006', 'L002');

-- Insert Research Interests
INSERT INTO research_interests (lecturer_id, research_area) VALUES
('L001', 'Machine Learning'),
('L001', 'Artificial Intelligence'),
('L002', 'Data Science'),
('L002', 'Big Data'),
('L003', 'Number Theory'),
('L004', 'Machine Learning'),
('L004', 'Natural Language Processing');
