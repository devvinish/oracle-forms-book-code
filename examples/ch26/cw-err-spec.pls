-- @where Library CW_LIB: package CW_ERR (Package Spec)
package cw_err is
  -- turns an error into a message for the user; call it from ON-ERROR
  procedure on_error;
  -- the constraint named in a database error: 'APPOINTMENTS_PATIENT_FK'
  function constraint_of(p_text varchar2) return varchar2;
end cw_err;
