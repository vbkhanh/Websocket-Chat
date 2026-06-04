/* Question 1 */
SELECT Department.DEPT_NAME, COUNT(Employee.EMP_ID) AS num_employees
FROM Employee
JOIN Department ON Employee.DEPT_ID = Department.DEPT_ID
WHERE Employee.EMP_SALARY > 7000
GROUP BY Department.DEPT_NAME;


/* Question 2 */
SELECT Department.DEPT_NAME, COUNT(Employee.EMP_ID) AS num_employees, AVG(Employee.EMP_SALARY) AS avg_salary
FROM Employee
JOIN Department ON Employee.DEPT_ID = Department.DEPT_ID
GROUP BY Departmen.DEPT_NAME
HAVING AVG(Employee.EMP_SALARY) > 7000;
