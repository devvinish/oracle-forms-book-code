-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.OPEN_DOC (form CH30_DOCUMENTS)
-- downloads the document to the client's temporary directory and opens it with the program the
-- client's desktop associates with its type
declare
  v_file   varchar2(500);
  v_cmd    varchar2(1000);
  v_os     varchar2(100) := webutil_clientinfo.get_operating_system;
  v_proc   webutil_host.process_id;
  v_err    webutil_host.output_array;
begin
  v_file := rtrim(webutil_clientinfo.get_system_property('java.io.tmpdir'),    -- '/tmp', or 'C:\...\Temp\'
                  webutil_clientinfo.get_file_separator)
            || webutil_clientinfo.get_file_separator || :docs.file_name;
  if not webutil_file_transfer.db_to_client(v_file, 'PATIENT_DOCUMENTS', 'CONTENT',
                                            'DOC_ID = ' || :docs.doc_id) then
    message('The download failed.');
    return;
  end if;
  v_cmd := case
             when v_os like 'Windows%' then 'cmd /c start "" "' || v_file || '"'
             when v_os like 'Mac%'     then 'open "' || v_file || '"'
             else 'xdg-open "' || v_file || '"'
           end;
  v_proc := webutil_host.blocking(v_cmd);
  if webutil_host.get_return_code(v_proc) <> 0 then
    v_err := webutil_host.get_standard_error(v_proc);
    message('Could not open ' || :docs.file_name || ' (exit code '
            || webutil_host.get_return_code(v_proc) || ')'
            || case when v_err.count > 0 then ': ' || v_err(v_err.first) end);
  end if;
  webutil_host.release_process(v_proc);
end;
