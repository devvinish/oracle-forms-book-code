-- @where Trigger: PRE-INSERT on PATIENTS
:patients.patient_id := patients_seq.nextval;
:patients.mrn        := 'CW' || to_char(100000 + (:patients.patient_id - 10000) * 7);
