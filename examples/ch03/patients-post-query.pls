-- @where Trigger: POST-QUERY on PATIENTS
:patients.age := age_in_years(:patients.birth_date);
