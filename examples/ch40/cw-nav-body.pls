-- @where Library CW_LIB: package CW_NAV (Package Body)
package body cw_nav is
  procedure start_form(p_user varchar2) is
  begin
    if cw_sec.username is null then            -- not signed in: a form run on its own, for testing
      cw_sec.login(p_user);
    end if;
    cw_sec.apply_menu;
    set_window_property(forms_mdi_window, TITLE,
                        'CareWell Clinic - ' || cw_sec.full_name || ' (' || initcap(cw_sec.app_role) || ')');
  end start_form;

  procedure open_module(p_form varchar2, p_patient_id number default null) is
  begin
    if p_patient_id is not null then
      cw_ctx.patient_id := p_patient_id;       -- shared: every form sees the same package data
    end if;
    if id_null(find_form(upper(p_form))) then
      open_form(p_form, activate, no_session, share_library_data);
    else
      go_form(upper(p_form));                  -- open already: its WHEN-FORM-NAVIGATE catches up
    end if;
  end open_module;
end cw_nav;
