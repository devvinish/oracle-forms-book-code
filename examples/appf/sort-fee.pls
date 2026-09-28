-- @where Trigger: WHEN-BUTTON-PRESSED on BTN.SORT_FEE (form APPF_NEW)
-- SORT_BLOCK sorts the records the block holds: fetch the rest first
go_block('DOCTORS');
last_record;
sort_block('DOCTORS.CONSULT_FEE', DESCENDING, NULLS_LAST);
first_record;                 -- the cursor stays with its record: go back to the top
