-- @ APPF_NEW: WHEN-BUTTON-PRESSED on SORT_FEE
-- SORT_BLOCK sorts the records the block holds: fetch the rest first
go_block('DOCTORS');
last_record;
sort_block('DOCTORS.CONSULT_FEE', DESCENDING, NULLS_LAST);
first_record;                 -- the cursor stays with its record: go back to the top
