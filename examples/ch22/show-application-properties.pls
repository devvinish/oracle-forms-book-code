-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
declare
  procedure show(p_name varchar2, p_value varchar2) is
  begin
    if :app.property is not null then
      create_record;
    end if;
    :app.property := p_name;
    :app.value    := p_value;
  end;
begin
  go_block('CTL');                   -- create the record of the check box
  go_block('APP');
  show('CURRENT_FORM',         get_application_property(current_form));
  show('CURRENT_FORM_NAME',    get_application_property(current_form_name));
  show('CONFIG',               get_application_property(config));
  show('CLIENT_DEPLOYMENT',    get_application_property(client_deployment));
  show('CLIENT_JAVA_VERSION',  get_application_property(client_java_version));
  show('VERSION',              get_application_property(version));
  show('OPERATING_SYSTEM',     get_application_property(operating_system));
  show('USER_INTERFACE',       get_application_property(user_interface));
  show('USERNAME',             get_application_property(username));
  show('CONNECT_STRING',       get_application_property(connect_string));
  show('DATASOURCE',           get_application_property(datasource));
  show('USER_NLS_LANG',        get_application_property(user_nls_lang));
  show('USER_NLS_DATE_FORMAT', get_application_property(user_nls_date_format));
  show('DISPLAY_WIDTH',        get_application_property(display_width));
  first_record;
  go_block('PATIENTS');
  execute_query;
end;
