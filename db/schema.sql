-- University Record Management System - schema (MySQL, 3NF)
-- CSCK542 Group C
-- Plural attributes (grades, qualifications, prerequisites, publications,
-- funding sources, etc.) are split into their own tables per 3NF.

DROP DATABASE IF EXISTS university_db;
CREATE DATABASE university_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE university_db;

CREATE TABLE departments (
    dept_id     INT AUTO_INCREMENT PRIMARY KEY,
    dept_name   VARCHAR(100) NOT NULL UNIQUE,
    faculty     VARCHAR(100) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE department_research_areas (
    dept_id        INT NOT NULL,
    research_area  VARCHAR(100) NOT NULL,
    PRIMARY KEY (dept_id, research_area),
    CONSTRAINT fk_dra_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
) ENGINE = InnoDB;

CREATE TABLE programs (
    program_id      INT AUTO_INCREMENT PRIMARY KEY,
    program_name    VARCHAR(100) NOT NULL,
    degree_awarded  VARCHAR(50) NOT NULL,
    duration_years  INT NOT NULL,
    dept_id         INT NOT NULL,
    CONSTRAINT chk_prog_duration CHECK (duration_years > 0),
    CONSTRAINT fk_prog_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
) ENGINE = InnoDB;

CREATE TABLE lecturers (
    lecturer_id  INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    dept_id      INT NOT NULL,
    course_load  INT NOT NULL DEFAULT 0,
    CONSTRAINT chk_lect_load CHECK (course_load >= 0),
    CONSTRAINT fk_lect_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
) ENGINE = InnoDB;

CREATE TABLE lecturer_qualifications (
    lecturer_id    INT NOT NULL,
    qualification  VARCHAR(150) NOT NULL,
    PRIMARY KEY (lecturer_id, qualification),
    CONSTRAINT fk_lq_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE lecturer_expertise (
    lecturer_id     INT NOT NULL,
    expertise_area  VARCHAR(100) NOT NULL,
    PRIMARY KEY (lecturer_id, expertise_area),
    CONSTRAINT fk_lx_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE lecturer_research_interests (
    lecturer_id  INT NOT NULL,
    interest     VARCHAR(100) NOT NULL,
    PRIMARY KEY (lecturer_id, interest),
    CONSTRAINT fk_lri_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

-- one-to-one: UNIQUE head_lecturer_id = a lecturer heads at most one group
CREATE TABLE research_groups (
    group_id          INT AUTO_INCREMENT PRIMARY KEY,
    group_name        VARCHAR(100) NOT NULL UNIQUE,
    head_lecturer_id  INT NOT NULL UNIQUE,
    CONSTRAINT fk_rg_head FOREIGN KEY (head_lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE committees (
    committee_id    INT AUTO_INCREMENT PRIMARY KEY,
    committee_name  VARCHAR(100) NOT NULL UNIQUE
) ENGINE = InnoDB;

CREATE TABLE committee_members (
    committee_id  INT NOT NULL,
    lecturer_id   INT NOT NULL,
    PRIMARY KEY (committee_id, lecturer_id),
    CONSTRAINT fk_cm_comm FOREIGN KEY (committee_id)
        REFERENCES committees (committee_id),
    CONSTRAINT fk_cm_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE students (
    student_id         INT AUTO_INCREMENT PRIMARY KEY,
    name               VARCHAR(100) NOT NULL,
    date_of_birth      DATE NOT NULL,
    email              VARCHAR(150) NOT NULL UNIQUE,
    phone              VARCHAR(20),
    program_id         INT NOT NULL,
    year_of_study      INT NOT NULL,
    graduation_status  VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    advisor_id         INT,
    CONSTRAINT chk_stud_year CHECK (year_of_study >= 1),
    CONSTRAINT chk_stud_status CHECK
        (graduation_status IN ('Enrolled', 'Graduated', 'Withdrawn')),
    CONSTRAINT fk_stud_prog FOREIGN KEY (program_id)
        REFERENCES programs (program_id),
    CONSTRAINT fk_stud_advisor FOREIGN KEY (advisor_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE disciplinary_records (
    record_id      INT AUTO_INCREMENT PRIMARY KEY,
    student_id     INT NOT NULL,
    incident_date  DATE NOT NULL,
    description    TEXT NOT NULL,
    outcome        VARCHAR(200),
    CONSTRAINT fk_disc_stud FOREIGN KEY (student_id)
        REFERENCES students (student_id)
) ENGINE = InnoDB;

CREATE TABLE student_organizations (
    org_id    INT AUTO_INCREMENT PRIMARY KEY,
    org_name  VARCHAR(100) NOT NULL UNIQUE
) ENGINE = InnoDB;

CREATE TABLE organization_memberships (
    student_id   INT NOT NULL,
    org_id       INT NOT NULL,
    joined_date  DATE,
    PRIMARY KEY (student_id, org_id),
    CONSTRAINT fk_om_stud FOREIGN KEY (student_id)
        REFERENCES students (student_id),
    CONSTRAINT fk_om_org FOREIGN KEY (org_id)
        REFERENCES student_organizations (org_id)
) ENGINE = InnoDB;

CREATE TABLE courses (
    course_code  VARCHAR(10) PRIMARY KEY,
    course_name  VARCHAR(100) NOT NULL,
    description  TEXT,
    dept_id      INT NOT NULL,
    level        INT NOT NULL,
    credits      INT NOT NULL,
    schedule     VARCHAR(100),
    CONSTRAINT chk_crs_level CHECK (level >= 1),
    CONSTRAINT chk_crs_credits CHECK (credits > 0),
    CONSTRAINT fk_crs_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
) ENGINE = InnoDB;

-- self-referencing junction
CREATE TABLE course_prerequisites (
    course_code  VARCHAR(10) NOT NULL,
    prereq_code  VARCHAR(10) NOT NULL,
    PRIMARY KEY (course_code, prereq_code),
    CONSTRAINT chk_pre_self CHECK (course_code <> prereq_code),
    CONSTRAINT fk_pre_course FOREIGN KEY (course_code)
        REFERENCES courses (course_code),
    CONSTRAINT fk_pre_prereq FOREIGN KEY (prereq_code)
        REFERENCES courses (course_code)
) ENGINE = InnoDB;

CREATE TABLE course_materials (
    material_id    INT AUTO_INCREMENT PRIMARY KEY,
    course_code    VARCHAR(10) NOT NULL,
    title          VARCHAR(200) NOT NULL,
    material_type  VARCHAR(50),
    CONSTRAINT fk_mat_course FOREIGN KEY (course_code)
        REFERENCES courses (course_code)
) ENGINE = InnoDB;

CREATE TABLE program_requirements (
    program_id   INT NOT NULL,
    course_code  VARCHAR(10) NOT NULL,
    PRIMARY KEY (program_id, course_code),
    CONSTRAINT fk_pr_prog FOREIGN KEY (program_id)
        REFERENCES programs (program_id),
    CONSTRAINT fk_pr_course FOREIGN KEY (course_code)
        REFERENCES courses (course_code)
) ENGINE = InnoDB;

-- lecturers teach courses per semester (joins to enrolments on course + semester)
CREATE TABLE teaching_assignments (
    lecturer_id  INT NOT NULL,
    course_code  VARCHAR(10) NOT NULL,
    semester     VARCHAR(10) NOT NULL,
    PRIMARY KEY (lecturer_id, course_code, semester),
    CONSTRAINT fk_ta_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id),
    CONSTRAINT fk_ta_course FOREIGN KEY (course_code)
        REFERENCES courses (course_code)
) ENGINE = InnoDB;

-- grades live here, per student/course/semester; NULL = in progress
CREATE TABLE enrolments (
    enrolment_id  INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT NOT NULL,
    course_code   VARCHAR(10) NOT NULL,
    semester      VARCHAR(10) NOT NULL,
    grade         DECIMAL(5, 2) NULL,
    CONSTRAINT uq_enrolment UNIQUE (student_id, course_code, semester),
    CONSTRAINT chk_enr_grade CHECK (grade BETWEEN 0 AND 100),
    CONSTRAINT fk_enr_stud FOREIGN KEY (student_id)
        REFERENCES students (student_id),
    CONSTRAINT fk_enr_course FOREIGN KEY (course_code)
        REFERENCES courses (course_code)
) ENGINE = InnoDB;

CREATE TABLE research_projects (
    project_id      INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    pi_lecturer_id  INT NOT NULL,
    outcomes        TEXT,
    CONSTRAINT fk_rp_pi FOREIGN KEY (pi_lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE project_funding (
    funding_id  INT AUTO_INCREMENT PRIMARY KEY,
    project_id  INT NOT NULL,
    source      VARCHAR(100) NOT NULL,
    amount      DECIMAL(12, 2),
    CONSTRAINT chk_pf_amount CHECK (amount >= 0),
    CONSTRAINT fk_pf_proj FOREIGN KEY (project_id)
        REFERENCES research_projects (project_id)
) ENGINE = InnoDB;

CREATE TABLE project_lecturers (
    project_id   INT NOT NULL,
    lecturer_id  INT NOT NULL,
    PRIMARY KEY (project_id, lecturer_id),
    CONSTRAINT fk_pl_proj FOREIGN KEY (project_id)
        REFERENCES research_projects (project_id),
    CONSTRAINT fk_pl_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id)
) ENGINE = InnoDB;

CREATE TABLE project_students (
    project_id  INT NOT NULL,
    student_id  INT NOT NULL,
    PRIMARY KEY (project_id, student_id),
    CONSTRAINT fk_ps_proj FOREIGN KEY (project_id)
        REFERENCES research_projects (project_id),
    CONSTRAINT fk_ps_stud FOREIGN KEY (student_id)
        REFERENCES students (student_id)
) ENGINE = InnoDB;

-- project_id nullable: a publication may not belong to a project
CREATE TABLE publications (
    pub_id       INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_id  INT NOT NULL,
    project_id   INT NULL,
    title        VARCHAR(200) NOT NULL,
    pub_year     INT NOT NULL,
    CONSTRAINT fk_pub_lect FOREIGN KEY (lecturer_id)
        REFERENCES lecturers (lecturer_id),
    CONSTRAINT fk_pub_proj FOREIGN KEY (project_id)
        REFERENCES research_projects (project_id)
) ENGINE = InnoDB;

CREATE TABLE non_academic_staff (
    staff_id                 INT AUTO_INCREMENT PRIMARY KEY,
    name                     VARCHAR(100) NOT NULL,
    job_title                VARCHAR(100) NOT NULL,
    dept_id                  INT NOT NULL,
    employment_type          VARCHAR(20) NOT NULL,
    contract_start           DATE NOT NULL,
    contract_end             DATE NULL,
    salary                   DECIMAL(10, 2),
    emergency_contact_name   VARCHAR(100),
    emergency_contact_phone  VARCHAR(20),
    CONSTRAINT chk_staff_type CHECK
        (employment_type IN ('Full-Time', 'Part-Time', 'Contract')),
    CONSTRAINT chk_staff_salary CHECK (salary >= 0),
    CONSTRAINT fk_staff_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
) ENGINE = InnoDB;
