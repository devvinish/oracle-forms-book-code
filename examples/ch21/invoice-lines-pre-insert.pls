-- @where Trigger: PRE-INSERT on INVOICE_LINES
declare
  v_id invoices.invoice_id%type;
begin
  -- lock the invoice: a second user adding lines to it waits here until this commit
  select invoice_id into v_id
  from   invoices
  where  invoice_id = :invoice_lines.invoice_id
  for update;

  select nvl(max(line_no), 0) + 1
  into   :invoice_lines.line_no
  from   invoice_lines
  where  invoice_id = :invoice_lines.invoice_id;
end;
