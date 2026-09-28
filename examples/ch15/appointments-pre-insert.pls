-- @where Trigger: PRE-INSERT on APPOINTMENTS
:appointments.appt_id := appointments_seq.nextval;
