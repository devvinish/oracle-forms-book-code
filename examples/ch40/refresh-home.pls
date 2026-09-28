-- @where Program unit: procedure REFRESH_HOME (form CW_MAIN)
procedure refresh_home is
  v_paid  number;
  v_total number;
begin
  :home.welcome := 'Welcome, ' || cw_sec.full_name;
  select count(*), count(case when status = 'CHECKED_IN' then 1 end)
    into :home.today_total, :home.checked_in
    from appointments
   where appt_start >= trunc(sysdate) and appt_start < trunc(sysdate) + 1
     and status <> 'CANCELLED';
  select count(*), nvl(sum(total_amount), 0) into :home.open_invoices, :home.open_amount
    from invoices where status in ('OPEN', 'PARTIAL');
  select nvl(sum(p.amount), 0) into v_paid from payments p;
  select nvl(sum(total_amount), 0) into v_total from invoices where status <> 'VOID';
  :home.collected := round(100 * v_paid / greatest(v_total, 1));
  -- the modules the user's role may use
  set_item_property('HOME.INVOICES', ENABLED,
                    case when cw_sec.has_role('ADMIN,BILLING') then PROPERTY_TRUE else PROPERTY_FALSE end);
end;
