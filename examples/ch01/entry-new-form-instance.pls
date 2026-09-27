-- @where Trigger: WHEN-NEW-FORM-INSTANCE on the form CH01_ENTRY
message('Form ' || get_application_property(current_form_name)
        || ', user ' || get_application_property(username)
        || ', on ' || get_application_property(operating_system));
