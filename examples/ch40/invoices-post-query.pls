-- @where Trigger: POST-QUERY on block INVOICES (form CW_BILLING)
select first_name || ' ' || last_name into :invoices.patient_name
  from patients where patient_id = :invoices.patient_id;
select nvl(sum(amount), 0) into :invoices.paid
  from payments where invoice_id = :invoices.invoice_id;
