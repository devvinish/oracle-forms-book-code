-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.IMPORT (form CH30_FEE_IMPORT)
-- reads new consultation fees from a CSV file on the user's computer (doctor_id,fee) into the block,
-- for the user to check before applying them
declare
  v_file varchar2(500);
  v_in   client_text_io.file_type;
  v_line varchar2(400);
  v_id   number;
  v_fee  number;
begin
  v_file := webutil_file.file_open_dialog('/work/transfer', null, '|CSV files (*.csv)|*.csv|',
                                          'Import new fees');
  if v_file is null then
    return;
  end if;
  go_block('FEES');
  clear_block(no_validate);
  v_in := client_text_io.fopen(v_file, 'r');
  client_text_io.get_line(v_in, v_line);            -- the header
  loop
    begin
      client_text_io.get_line(v_in, v_line);
    exception
      when no_data_found then exit;                  -- the end of the file
    end;
    if :fees.doctor_id is not null then
      create_record;
    end if;
    begin
      v_id  := to_number(substr(v_line, 1, instr(v_line, ',') - 1));
      v_fee := to_number(substr(v_line, instr(v_line, ',') + 1));
      :fees.doctor_id := v_id;
      :fees.new_fee   := v_fee;
      select first_name || ' ' || last_name, consult_fee into :fees.doctor_name, :fees.old_fee
        from doctors where doctor_id = v_id;
      :fees.note := case when v_fee = :fees.old_fee then 'unchanged'
                         when v_fee < 0 then 'negative: skipped'
                         else to_char(round(100 * (v_fee - :fees.old_fee) / :fees.old_fee), 'FMS990') || '%' end;
    exception
      when no_data_found then :fees.note := 'no such doctor: skipped';
      when value_error then   :fees.note := 'not a number: ' || v_line;
    end;
  end loop;
  client_text_io.fclose(v_in);
  first_record;
end;
