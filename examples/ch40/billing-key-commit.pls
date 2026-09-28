-- @where Trigger: KEY-COMMIT (form CW_BILLING)
-- after the save, query the invoices again: POST-INSERT changed an invoice's status in the database
declare
  v_id     invoices.invoice_id%type := :invoices.invoice_id;
  v_status invoices.status%type;
begin
  :system.message_level := '5';          -- the message below replaces FRM-40400
  commit_form;
  :system.message_level := '0';
  if :system.form_status = 'QUERY' then
    select status into v_status from invoices where invoice_id = v_id;
    go_block('INVOICES');
    execute_query;
    -- a patient's invoices: back to the one just paid (in the list to be paid, it is gone)
    if :ctl.patient_id is not null then
      loop
        exit when :invoices.invoice_id = v_id or :system.last_record = 'TRUE';
        next_record;
      end loop;
    end if;
    message('Saved. Invoice ' || v_id || ' is ' || v_status || '.');
  end if;
end;
