-- @where Trigger: POST-QUERY on DEPARTMENTS
select first_name || ' ' || last_name
into   :departments.head_name
from   doctors
where  doctor_id = :departments.head_doctor;
