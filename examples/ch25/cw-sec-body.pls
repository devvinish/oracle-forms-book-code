-- @where Library CW_LIB: package CW_SEC (Package Body)
package body cw_sec is
  procedure login(p_username varchar2) is
  begin
    select username, full_name, app_role into username, full_name, app_role
      from app_users
     where username = upper(p_username) and active = 'Y';
    copy(username, 'GLOBAL.CW_USER');                   -- for menu code and other forms
  exception
    when no_data_found then
      cw_msg.fail('Unknown or inactive user: ' || p_username);
  end login;

  function has_role(p_roles varchar2) return boolean is
  begin
    return instr(',' || upper(p_roles) || ',', ',' || app_role || ',') > 0;
  end has_role;

  procedure apply_menu is
    procedure allow(p_item varchar2, p_roles varchar2) is
      v_item menuitem := find_menu_item(p_item);
    begin
      if not id_null(v_item) and not has_role(p_roles) then
        set_menu_item_property(v_item, enabled, property_false);   -- only ever disable
      end if;
    end allow;
  begin
    allow('CLINIC.INVOICES', 'ADMIN,BILLING');
    allow('CLINIC.FEES', 'ADMIN');
    allow('RECORDS.DELETE', 'ADMIN,RECEPTION');
  end apply_menu;
end cw_sec;
