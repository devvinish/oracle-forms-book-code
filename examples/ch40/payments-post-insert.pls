-- @where Trigger: POST-INSERT on block PAYMENTS (form CW_BILLING)
-- the invoice's status follows its payments, in the same transaction as the payment
declare
  v_paid  number;
begin
  select nvl(sum(amount), 0) into v_paid from payments where invoice_id = :payments.invoice_id;
  update invoices
     set status = case when v_paid >= total_amount then 'PAID' else 'PARTIAL' end
   where invoice_id = :payments.invoice_id;
end;
