-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.ADD_DOC (form CH30_DOCUMENTS)
-- stores a file of the user's in PATIENT_DOCUMENTS.CONTENT: first the row, then its BLOB
declare
  v_file varchar2(500);
  v_id   number;
begin
  v_file := webutil_file.file_open_dialog('/work/transfer', null, '|All files (*.*)|*.*|',
              'Add a document for ' || :patients.first_name || ' ' || :patients.last_name);
  if v_file is null then
    return;
  end if;
  go_block('DOCS');
  last_record;
  if :docs.doc_id is not null then
    create_record;
  end if;
  select documents_seq.nextval into v_id from dual;
  :docs.doc_id    := v_id;
  :docs.file_name := substr(v_file, greatest(instr(v_file, '/', -1), instr(v_file, '\', -1)) + 1);
  :docs.doc_type  := nvl(:ctl.doc_type, 'OTHER');
  :docs.file_size := webutil_file.file_size(v_file);
  :docs.uploaded_on := sysdate;            -- Forms inserts every item of the block: a null would
  :docs.uploaded_by := user;               -- override the columns' DEFAULT, and they are NOT NULL
  :system.message_level := '5';           -- no FRM-40404 for the POST
  post;                                   -- the row must exist before WebUtil fills its BLOB
  :system.message_level := '0';
  if not form_success then
    return;                               -- Forms has shown why the row couldn't be written
  end if;
  if webutil_file_transfer.client_to_db(v_file, 'PATIENT_DOCUMENTS', 'CONTENT', 'DOC_ID = ' || v_id) then
    commit_form;                          -- the row and its content, in one transaction
  else
    message('The upload failed; nothing was saved.');
    clear_form(no_commit, full_rollback); -- rolls back the posted row
  end if;
end;
