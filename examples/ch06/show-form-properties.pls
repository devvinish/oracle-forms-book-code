-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form
declare
  frm varchar2(30) := :system.current_form;

  procedure show(p_property varchar2, p_value varchar2) is
  begin
    if :props.property is not null then
      create_record;                        -- a new row for each property after the first
    end if;
    :props.property := p_property;
    :props.value    := p_value;
  end;
begin
  go_block('PROPS');
  show('FORM_NAME',              get_form_property(frm, form_name));
  show('FILE_NAME',              get_form_property(frm, file_name));
  show('FIRST_NAVIGATION_BLOCK', get_form_property(frm, first_navigation_block));
  show('VALIDATION_UNIT',        get_form_property(frm, validation_unit));
  show('INTERACTION_MODE',       get_form_property(frm, interaction_mode));
  show('ISOLATION_MODE',         get_form_property(frm, isolation_mode));
  show('MAX_QUERY_TIME',         get_form_property(frm, max_query_time));
  show('MAX_RECORDS_FETCHED',    get_form_property(frm, max_records_fetched));
  show('CURSOR_MODE',            get_form_property(frm, cursor_mode));
  show('SAVEPOINT_MODE',         get_form_property(frm, savepoint_mode));
  show('COORDINATE_SYSTEM',      get_form_property(frm, coordinate_system));
  show('MODULE_NLS_LANG',        get_form_property(frm, module_nls_lang));
  first_record;
end;
