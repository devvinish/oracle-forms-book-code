-- @where Trigger: PRE-INSERT on block APPOINTMENTS (form CH39_BOOKING)
:appointments.appt_id := appointments_seq.nextval;
check_double_booking;          -- again: sees the records this save has already posted
