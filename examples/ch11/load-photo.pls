-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.LOAD_PHOTO
declare
  v_file varchar2(200) := '/work/images/patients/' || :patients.mrn || '.jpg';
begin
  read_image_file(v_file, 'JFIF', 'PATIENTS.PHOTO');
  if not form_success then
    message('There is no photo file for ' || :patients.mrn || '.');
  end if;
end;
