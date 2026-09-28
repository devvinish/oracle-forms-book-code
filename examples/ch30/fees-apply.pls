-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.APPLY (form CH30_FEE_IMPORT)
declare
  v_n pls_integer := 0;
begin
  go_block('FEES');
  first_record;
  loop
    if :fees.note like '%\%' escape '\' then       -- a real change
      update doctors set consult_fee = :fees.new_fee where doctor_id = :fees.doctor_id;
      v_n := v_n + 1;
    end if;
    exit when :system.last_record = 'TRUE';
    next_record;
  end loop;
  forms_ddl('commit');                             -- the block isn't a database block: commit the updates
  message(v_n || ' fees changed.');
end;
