-- @where Library CW_LIB: package CW_NAV (Package Spec)
package cw_nav is
  -- the start of every CareWell form: the signed-in user, or the form's P_USER when it runs alone
  procedure start_form(p_user varchar2);
  -- opens a module, or brings it to the front, for a patient (null: the current one)
  procedure open_module(p_form varchar2, p_patient_id number default null);
end cw_nav;
