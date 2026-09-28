-- @where Trigger: WHEN-BUTTON-PRESSED on TOOLS.INFO
message('Client: ' || webutil_clientinfo.get_operating_system
        || ', user ' || webutil_clientinfo.get_user_name
        || ', host ' || webutil_clientinfo.get_host_name
        || ', Java ' || webutil_clientinfo.get_java_version);
