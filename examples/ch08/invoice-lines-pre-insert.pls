-- @where Trigger: PRE-INSERT on INVOICE_LINES
select nvl(max(line_no), 0) + 1
into   :invoice_lines.line_no
from   invoice_lines
where  invoice_id = :invoice_lines.invoice_id;
