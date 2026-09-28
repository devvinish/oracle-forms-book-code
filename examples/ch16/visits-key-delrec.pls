-- @where Trigger: KEY-DELREC on VISITS
declare
  v_invoice invoices.invoice_id%type;
  v_rx      number;
  v_button  number;
begin
  begin
    select invoice_id into v_invoice
    from   invoices
    where  visit_id = :visits.visit_id and rownum = 1;
  exception
    when no_data_found then v_invoice := null;
  end;

  if v_invoice is not null then
    set_alert_property('AL_CANNOT_DELETE', alert_message_text,
      'Visit ' || :visits.visit_id || ' is billed on invoice ' || v_invoice ||
      '. It can''t be deleted.');
    v_button := show_alert('AL_CANNOT_DELETE');
    raise form_trigger_failure;
  end if;

  select count(*) into v_rx from prescriptions where visit_id = :visits.visit_id;
  set_alert_property('AL_CONFIRM_DELETE', alert_message_text,
    'Delete the visit of ' || to_char(:visits.visit_date, 'DD-MON-YYYY') ||
    ' and its ' || v_rx || ' prescriptions?');
  if show_alert('AL_CONFIRM_DELETE') = alert_button1 then
    delete_record;
  end if;
end;
