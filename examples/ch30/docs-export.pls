-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.EXPORT (form CH30_DOCUMENTS)
-- the list written on the server (EXPORT_BLOCK of Chapter 39), then sent to the user in one transfer
declare
  v_server varchar2(200) := '/work/transfer/out/documents_' || :patients.mrn || '.csv';
  v_client varchar2(500);
begin
  v_client := webutil_file.file_save_dialog('/work/transfer', 'documents_' || :patients.mrn || '.csv',
                                            '|CSV files (*.csv)|*.csv|', 'Export the list of documents');
  if v_client is null then
    return;
  end if;
  export_block('DOCS', v_server);
  if webutil_file_transfer.as_to_client(v_client, v_server) then
    message('Exported to ' || v_client);
  end if;
end;
