-- @where Program unit: procedure LOAD_INVOICES (form CW_BILLING)
-- the invoices of the current patient, or, without one, every invoice still to be paid
procedure load_invoices is
begin
  if nvl(cw_ctx.patient_id, -1) = nvl(:ctl.patient_id, -1) and :system.mode = 'NORMAL'
     and :invoices.invoice_id is not null then
    return;                              -- already showing them
  end if;
  :ctl.patient_id := cw_ctx.patient_id;
  if :ctl.patient_id is null then
    :ctl.showing := 'Invoices to be paid';
    set_block_property('INVOICES', DEFAULT_WHERE, 'status in (''OPEN'', ''PARTIAL'')');
  else
    select 'Invoices of ' || first_name || ' ' || last_name into :ctl.showing
      from patients where patient_id = :ctl.patient_id;
    set_block_property('INVOICES', DEFAULT_WHERE, 'patient_id = :ctl.patient_id');
  end if;
  go_block('INVOICES');
  execute_query;
end;
