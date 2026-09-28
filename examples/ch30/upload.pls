-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.UPLOAD
declare
  v_client varchar2(500);
  v_server varchar2(500);
begin
  v_client := webutil_file.file_open_dialog('/work/transfer', null, null,
                                            'Send a file to the clinic');
  if v_client is null then
    return;
  end if;
  v_server := '/work/transfer/in/' || :patients.mrn || '_'
              || substr(v_client, instr(v_client, '/', -1) + 1);
  if webutil_file_transfer.client_to_as(v_client, v_server) then
    message('Stored on the server as ' || v_server);
  else
    message('The transfer failed.');
  end if;
end;
