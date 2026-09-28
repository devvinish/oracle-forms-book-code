-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.EXPORT
declare
  v_name varchar2(500);
  v_out  client_text_io.file_type;
  v_n    pls_integer := 0;
begin
  v_name := webutil_file.file_save_dialog('/work/transfer', 'patients.csv',
                                          '|CSV files (*.csv)|*.csv|', 'Export patients');
  if v_name is null then
    return;
  end if;
  v_out := client_text_io.fopen(v_name, 'w');       -- a file on the user's computer
  client_text_io.put_line(v_out, 'MRN,FIRST_NAME,LAST_NAME,PHONE');
  for p in (select mrn, first_name, last_name, phone from patients
             where city = 'Pune' order by last_name, first_name) loop
    client_text_io.put_line(v_out, p.mrn || ',' || p.first_name || ',' || p.last_name
                                   || ',' || p.phone);
    v_n := v_n + 1;
  end loop;
  client_text_io.fclose(v_out);
  message(v_n || ' patients written to ' || v_name);
end;
