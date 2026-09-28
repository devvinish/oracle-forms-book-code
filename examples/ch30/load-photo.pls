-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.LOAD_PHOTO
declare
  v_file varchar2(500);
begin
  v_file := webutil_file.file_open_dialog(
              directory_name => '/work/images/patients',   -- on the user's computer
              file_filter    => '|JPEG images (*.jpg)|*.jpg|',
              title          => 'Photo of ' || :patients.first_name || ' '
                                || :patients.last_name);
  if v_file is null then
    return;                                             -- the user cancelled
  end if;
  client_image.read_image_file(v_file, 'JPEG', 'PATIENTS.PHOTO');
  message('Loaded ' || v_file || ' (' || webutil_file.file_size(v_file)
          || ' bytes). Save to keep it.');
end;
