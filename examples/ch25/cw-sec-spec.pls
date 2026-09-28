-- @where Library CW_LIB: package CW_SEC (Package Spec)
package cw_sec is
  -- the user of the application, from APP_USERS (every user connects as CAREWELL)
  username  varchar2(30);
  full_name varchar2(60);
  app_role  varchar2(20);
  procedure login(p_username varchar2);
  function has_role(p_roles varchar2) return boolean;  -- has_role('ADMIN,BILLING')
  procedure apply_menu;                    -- disables what the role may not use
end cw_sec;
