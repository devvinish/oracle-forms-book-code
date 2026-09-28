-- @where Library CW_LIB: procedure STAMP_CITY
procedure stamp_city(p_block varchar2) is
begin
  if name_in(p_block || '.CITY') is null then             -- read :<block>.city
    copy(name_in('GLOBAL.CW_CITY'), p_block || '.CITY');   -- write it from :global.cw_city
  end if;
end stamp_city;
