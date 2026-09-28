-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.REPEAT (form CH39_VISIT)
-- copies the prescription of the patient's previous visit into this visit, as new records to check and save
declare
  v_prev  visits.visit_id%type;
  v_date  date;
  v_n     pls_integer := 0;
begin
  if :visits.visit_id is null then
    message('Save the visit first.');
    return;
  end if;
  for v in (select visit_id, visit_date from visits v
             where patient_id = :visits.patient_id and visit_date < :visits.visit_date
               and exists (select null from prescriptions r where r.visit_id = v.visit_id)
             order by visit_date desc) loop
    v_prev := v.visit_id;
    v_date := v.visit_date;
    exit;                                   -- the latest one
  end loop;
  if v_prev is null then
    message('No earlier prescription for this patient.');
    return;
  end if;
  go_block('PRESCRIPTIONS');
  last_record;                              -- after the lines the visit already has
  for r in (select r.medicine_id, m.medicine_name, r.dosage, r.frequency, r.days, r.quantity
              from prescriptions r, medicines m
             where m.medicine_id = r.medicine_id and r.visit_id = v_prev
             order by r.rx_id) loop
    if :prescriptions.medicine_id is not null then
      create_record;
    end if;
    :prescriptions.medicine_id   := r.medicine_id;
    :prescriptions.medicine_name := r.medicine_name;
    :prescriptions.dosage        := r.dosage;
    :prescriptions.frequency     := r.frequency;
    :prescriptions.days          := r.days;
    :prescriptions.quantity      := r.quantity;
    v_n := v_n + 1;
  end loop;
  first_record;
  message(v_n || ' lines copied from the visit of ' || to_char(v_date, 'DD-MON-YYYY')
          || '. Check them and save.');
end;
