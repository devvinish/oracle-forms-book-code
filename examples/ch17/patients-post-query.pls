-- @where Trigger: POST-QUERY on PATIENTS
:patients.age     := cw_util.age_in_years(:patients.birth_date);   -- a form program unit
:patients.summary := cw_api.patient_summary(:patients.patient_id); -- a stored function
