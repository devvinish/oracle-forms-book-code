-- @where Trigger: ON-DELETE on block DOCTORS (form CH39_DOCTORS)
-- a deleted doctor is only marked inactive: appointments, visits, and invoices still refer to the row
update doctors set active = 'N' where doctor_id = :doctors.doctor_id;
