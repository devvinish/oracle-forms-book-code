-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.SAVE_DOC (form CH30_DOCUMENTS)
declare
  v_file varchar2(500);
begin
  v_file := webutil_file.file_save_dialog('/work/transfer', :docs.file_name, null, 'Save the document as');
  if v_file is not null and webutil_file_transfer.db_to_client(v_file,
       'PATIENT_DOCUMENTS', 'CONTENT', 'DOC_ID = ' || :docs.doc_id) then
    message('Saved as ' || v_file);
  end if;
end;
