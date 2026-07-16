-- University Record Management System - seed data
-- Current semester = '2026-S1'; NULL grade = in progress

USE university_db;

INSERT INTO departments (dept_id, dept_name, faculty) VALUES
(1, 'Computer Science', 'Science & Engineering'),
(2, 'Mathematics',      'Science & Engineering'),
(3, 'Business',         'Humanities & Social Sciences');

INSERT INTO department_research_areas (dept_id, research_area) VALUES
(1, 'Machine Learning'), (1, 'Distributed Systems'), (1, 'Cyber Security'),
(2, 'Statistics'), (2, 'Applied Mathematics'),
(3, 'Finance'), (3, 'Marketing Analytics');

INSERT INTO programs (program_id, program_name, degree_awarded, duration_years, dept_id) VALUES
(1, 'Computer Science',           'BSc (Hons)', 3, 1),
(2, 'Data Science & AI',          'MSc',        2, 1),
(3, 'Mathematics with Finance',   'BSc (Hons)', 3, 2);

INSERT INTO lecturers (lecturer_id, name, email, dept_id, course_load) VALUES
(1, 'Dr Sara Haddad',    'sara.haddad@uni.ac.uk',    1, 3),
(2, 'Prof Omar Farouk',  'omar.farouk@uni.ac.uk',    1, 2),
(3, 'Dr Emily Watson',   'emily.watson@uni.ac.uk',   2, 3),
(4, 'Dr James Okafor',   'james.okafor@uni.ac.uk',   2, 2),
(5, 'Dr Lina Costa',     'lina.costa@uni.ac.uk',     3, 2),
(6, 'Prof David Chen',   'david.chen@uni.ac.uk',     1, 1);

INSERT INTO lecturer_qualifications (lecturer_id, qualification) VALUES
(1, 'PhD Computer Science'), (1, 'MSc Software Engineering'),
(2, 'PhD Artificial Intelligence'),
(3, 'PhD Statistics'), (3, 'FHEA'),
(4, 'PhD Applied Mathematics'),
(5, 'PhD Finance'), (5, 'MBA'),
(6, 'PhD Distributed Computing');

INSERT INTO lecturer_expertise (lecturer_id, expertise_area) VALUES
(1, 'Machine Learning'), (1, 'Data Mining'),
(2, 'Machine Learning'), (2, 'Natural Language Processing'),
(3, 'Statistics'), (3, 'Bayesian Inference'),
(4, 'Optimisation'), (4, 'Numerical Methods'),
(5, 'Corporate Finance'), (5, 'Risk Modelling'),
(6, 'Distributed Systems'), (6, 'Cloud Computing');

INSERT INTO lecturer_research_interests (lecturer_id, interest) VALUES
(1, 'Explainable AI'), (2, 'Large Language Models'),
(3, 'Statistical Learning'), (4, 'Convex Optimisation'),
(5, 'Algorithmic Trading'), (6, 'Edge Computing');

INSERT INTO research_groups (group_id, group_name, head_lecturer_id) VALUES
(1, 'Intelligent Systems Lab', 2),
(2, 'Statistical Modelling Group', 3),
(3, 'Distributed Computing Lab', 6);

INSERT INTO committees (committee_id, committee_name) VALUES
(1, 'Ethics Committee'), (2, 'Curriculum Board'), (3, 'Admissions Panel');

INSERT INTO committee_members (committee_id, lecturer_id) VALUES
(1, 1), (1, 3), (2, 2), (2, 4), (2, 5), (3, 6);

INSERT INTO students (student_id, name, date_of_birth, email, phone,
                      program_id, year_of_study, graduation_status, advisor_id) VALUES
(1001, 'Amira Khalil',   '2004-03-12', 'a.khalil@student.uni.ac.uk',   '07700 900101', 1, 3, 'Enrolled', 1),
(1002, 'Ben Carter',     '2004-07-25', 'b.carter@student.uni.ac.uk',   '07700 900102', 1, 3, 'Enrolled', 1),
(1003, 'Chloe Nguyen',   '2005-01-08', 'c.nguyen@student.uni.ac.uk',   '07700 900103', 1, 2, 'Enrolled', 2),
(1004, 'Daniel Adeyemi', '2005-11-30', 'd.adeyemi@student.uni.ac.uk',  '07700 900104', 1, 2, 'Enrolled', 2),
(1005, 'Eva Kowalski',   '2006-05-17', 'e.kowalski@student.uni.ac.uk', '07700 900105', 1, 1, 'Enrolled', 6),
(1006, 'Faris Mansour',  '2003-09-02', 'f.mansour@student.uni.ac.uk',  '07700 900106', 3, 3, 'Enrolled', 4),
(1007, 'Grace Osei',     '2004-12-19', 'g.osei@student.uni.ac.uk',     '07700 900107', 3, 3, 'Enrolled', 3),
(1008, 'Hassan Ali',     '2000-04-06', 'h.ali@student.uni.ac.uk',      '07700 900108', 2, 2, 'Enrolled', 2),
(1009, 'Isla McGregor',  '2001-08-23', 'i.mcgregor@student.uni.ac.uk', '07700 900109', 2, 1, 'Enrolled', 1),
(1010, 'Jakub Novak',    '2002-02-14', 'j.novak@student.uni.ac.uk',    '07700 900110', 3, 3, 'Withdrawn', 3);

INSERT INTO disciplinary_records (record_id, student_id, incident_date, description, outcome) VALUES
(1, 1004, '2025-11-03', 'Plagiarism flag on coursework', 'Formal warning'),
(2, 1010, '2025-10-15', 'Repeated non-attendance', 'Case closed - student withdrew');

INSERT INTO student_organizations (org_id, org_name) VALUES
(1, 'Computing Society'), (2, 'Football Club'), (3, 'Investment Society');

INSERT INTO organization_memberships (student_id, org_id, joined_date) VALUES
(1001, 1, '2023-10-01'), (1001, 2, '2023-10-05'),
(1002, 2, '2023-10-02'), (1003, 1, '2024-10-01'),
(1006, 3, '2023-10-11'), (1007, 3, '2023-10-12'),
(1008, 1, '2025-10-01');

INSERT INTO courses (course_code, course_name, description, dept_id, level, credits, schedule) VALUES
('CS101', 'Programming Fundamentals', 'Intro to programming in Python.',        1, 1, 20, 'Mon 09:00, Thu 11:00'),
('CS201', 'Databases',                'Relational design, SQL, normalisation.', 1, 2, 20, 'Tue 10:00, Fri 09:00'),
('CS301', 'Machine Learning',         'Supervised and unsupervised learning.',  1, 3, 20, 'Wed 14:00'),
('CS302', 'Distributed Systems',      'Consistency, replication, consensus.',   1, 3, 20, 'Mon 13:00'),
('MA101', 'Calculus I',               'Limits, derivatives, integrals.',        2, 1, 20, 'Tue 09:00'),
('MA201', 'Statistics',               'Probability and statistical inference.', 2, 2, 20, 'Thu 10:00'),
('MA301', 'Financial Mathematics',    'Derivatives pricing, risk.',             2, 3, 20, 'Fri 11:00'),
('BU201', 'Corporate Finance',        'Capital structure and valuation.',       3, 2, 20, 'Wed 10:00');

INSERT INTO course_prerequisites (course_code, prereq_code) VALUES
('CS201', 'CS101'), ('CS301', 'CS201'), ('CS302', 'CS201'),
('MA201', 'MA101'), ('MA301', 'MA201');

INSERT INTO course_materials (material_id, course_code, title, material_type) VALUES
(1, 'CS201', 'Database Systems: The Complete Book', 'Textbook'),
(2, 'CS201', 'Week 1-5 Lecture Slides', 'Slides'),
(3, 'CS301', 'Pattern Recognition and ML', 'Textbook'),
(4, 'MA201', 'Statistics Problem Sets', 'Worksheet');

INSERT INTO program_requirements (program_id, course_code) VALUES
(1, 'CS101'), (1, 'CS201'), (1, 'CS301'), (1, 'CS302'),
(2, 'CS301'), (2, 'MA201'),
(3, 'MA101'), (3, 'MA201'), (3, 'MA301'), (3, 'BU201');

INSERT INTO teaching_assignments (lecturer_id, course_code, semester) VALUES
(1, 'CS301', '2026-S1'), (1, 'CS201', '2026-S1'),
(2, 'CS301', '2025-S2'), (2, 'CS101', '2026-S1'),
(3, 'MA201', '2026-S1'), (3, 'MA101', '2025-S2'),
(4, 'MA301', '2026-S1'), (4, 'MA101', '2026-S1'),
(5, 'BU201', '2026-S1'),
(6, 'CS302', '2026-S1');

INSERT INTO enrolments (student_id, course_code, semester, grade) VALUES
(1001, 'CS101', '2025-S1', 82), (1001, 'CS201', '2025-S2', 78),
(1001, 'CS301', '2026-S1', NULL), (1001, 'CS302', '2026-S1', NULL),
(1002, 'CS101', '2025-S1', 74), (1002, 'CS201', '2025-S2', 71),
(1002, 'CS301', '2026-S1', NULL),
(1003, 'CS101', '2025-S1', 65), (1003, 'CS201', '2026-S1', NULL),
(1004, 'CS101', '2025-S1', 58), (1004, 'CS201', '2026-S1', NULL),
(1005, 'CS101', '2026-S1', NULL),
(1006, 'MA101', '2025-S1', 88), (1006, 'MA201', '2025-S2', 91),
(1006, 'MA301', '2026-S1', NULL),
(1007, 'MA101', '2025-S1', 69), (1007, 'MA201', '2025-S2', 72),
(1007, 'MA301', '2026-S1', NULL), (1007, 'BU201', '2026-S1', NULL),
(1008, 'CS301', '2025-S2', 84),
(1009, 'MA201', '2025-S2', 76),
(1010, 'MA101', '2025-S1', 44);

INSERT INTO research_projects (project_id, title, pi_lecturer_id, outcomes) VALUES
(1, 'Explainable AI for Credit Scoring',      1, 'Prototype delivered; paper under review'),
(2, 'Federated Learning at the Edge',         6, 'Ongoing'),
(3, 'Bayesian Methods for Clinical Trials',   3, 'Two publications');

INSERT INTO project_funding (funding_id, project_id, source, amount) VALUES
(1, 1, 'UKRI', 120000), (2, 1, 'Industry Partner', 30000),
(3, 2, 'EPSRC', 250000),
(4, 3, 'Wellcome Trust', 90000);

INSERT INTO project_lecturers (project_id, lecturer_id) VALUES
(1, 1), (1, 2), (2, 6), (2, 1), (3, 3), (3, 4);

INSERT INTO project_students (project_id, student_id) VALUES
(1, 1001), (1, 1008), (2, 1002), (3, 1006), (3, 1007);

INSERT INTO publications (pub_id, lecturer_id, project_id, title, pub_year) VALUES
(1, 1, 1,    'SHAP-Based Explanations in Credit Models',      2026),
(2, 2, NULL, 'Prompt Engineering for Domain LLMs',            2025),
(3, 3, 3,    'Adaptive Bayesian Trial Designs',               2026),
(4, 3, 3,    'Priors in Small-Sample Clinical Studies',       2025),
(5, 6, 2,    'Consensus Protocols on Edge Devices',           2026),
(6, 4, NULL, 'Convergence Rates in Convex Optimisation',      2024);

INSERT INTO non_academic_staff (staff_id, name, job_title, dept_id, employment_type,
                                contract_start, contract_end, salary,
                                emergency_contact_name, emergency_contact_phone) VALUES
(1, 'Priya Sharma',  'Department Administrator', 1, 'Full-Time', '2019-09-01', NULL,        32000, 'Raj Sharma',   '07700 900201'),
(2, 'Tom Bailey',    'Lab Technician',           1, 'Full-Time', '2021-01-15', NULL,        28500, 'Sue Bailey',   '07700 900202'),
(3, 'Nadia Hussein', 'Finance Officer',          3, 'Part-Time', '2022-06-01', NULL,        21000, 'Ali Hussein',  '07700 900203'),
(4, 'Mark Ellis',    'IT Support Analyst',       1, 'Contract',  '2025-09-01', '2026-08-31', 30000, 'Jane Ellis',  '07700 900204'),
(5, 'Sofia Rossi',   'Student Services Advisor', 2, 'Full-Time', '2020-03-01', NULL,        27000, 'Marco Rossi', '07700 900205');
