SELECT * FROM exercise1.emp_1;
ALTER TABLE exercise1.emp_1 CHANGE EMP_Lname EMP_LNAME VARCHAR(45);
SET SQL_SAFE_UPDATES = 0;
UPDATE exercise1.emp_1 SET EMP_NUM = "101" , EMP_LNAME = "Nevas", EMP_FNAME = "John", EMP_INITIAL = "G", EMP_HIREDATE = "94-11-08" 
WHERE EMP_NUM = "101";
UPDATE exercise1.emp_1 SET EMP_NUM = "102", EMP_LNAME = "Senior", EMP_FNAME = "David", EMP_INITIAL = "H",  EMP_HIREDATE = "87-07-12", JOB_CODE = "501"
WHERE JOB_CODE = "503";
UPDATE exercise1.emp_1 SET EMP_NUM = "103", EMP_LNAME = "Arbos", EMP_FNAME = "June", EMP_INITIAL = "E",  EMP_HIREDATE = "96-12-01", JOB_CODE = "500"
WHERE JOB_CODE = "504";
INSERT INTO exercise1.emp_1 (EMP_NUM, EMP_LNAME, EMP_FNAME, EMP_INITIAL, EMP_HIREDATE, JOB_CODE)
VALUES 
('104', 'Ramoras', 'Anne', 'K', '1998-11-15', 501),
('105', 'Joson', 'Alice', 'P', '1993-02-01', 502),
('106', 'Smith', 'William', 'D', '1990-06-23', 500),
('107', 'Alonso', 'Mara', 'F', '1991-10-10', 500),
('108', 'Washington', 'Raf', 'S', '1989-08-22', 501),
('109', 'Field', 'Larry', 'W', '1999-07-18', 501);

UPDATE exercise1.emp_1 SET JOB_CODE = "501" WHERE EMP_NUM = "106";
DELETE from exercise1.emp_1 WHERE EMP_NUM = "106";


