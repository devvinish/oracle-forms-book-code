-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.DETAILS (form CH30_DOCUMENTS)
-- runs a program on the client and reads what it printed: the SHA-256 checksum of the document
declare
  v_file varchar2(500);
  v_cmd  varchar2(600);
  v_proc webutil_host.process_id;
  v_out  webutil_host.output_array;
begin
  v_file := rtrim(webutil_clientinfo.get_system_property('java.io.tmpdir'), webutil_clientinfo.get_file_separator)
            || webutil_clientinfo.get_file_separator || :docs.file_name;
  if not webutil_file_transfer.db_to_client(v_file, 'PATIENT_DOCUMENTS', 'CONTENT',
                                            'DOC_ID = ' || :docs.doc_id) then
    return;
  end if;
  v_cmd := case when webutil_clientinfo.get_operating_system like 'Mac%'
                then 'shasum -a 256 ' else 'sha256sum ' end || v_file;
  v_proc := webutil_host.blocking(v_cmd);
  v_out  := webutil_host.get_standard_output(v_proc);
  if v_out.count > 0 then
    message('SHA-256 of ' || :docs.file_name || ': ' || substr(v_out(v_out.first), 1, 64));
  end if;
  webutil_host.release_process(v_proc);
end;
