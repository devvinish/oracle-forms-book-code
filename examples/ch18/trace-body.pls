-- @where Program unit: TRACE (Package Body)
package body trace is
  g_count pls_integer := 0;

  procedure log(p_trigger varchar2) is
    f      text_io.file_type;
    v_what varchar2(80);
  begin
    g_count := g_count + 1;
    v_what  := nvl(:system.trigger_item, :system.trigger_block);
    if :system.trigger_record is not null and :system.trigger_block is not null then
      v_what := v_what || ' (record ' || :system.trigger_record || ')';
    end if;
    -- the first line of the session creates the file, the others are appended
    f := text_io.fopen('/tmp/ch18_trace.txt',
                       case when g_count = 1 then 'w' else 'a' end);
    text_io.put_line(f, lpad(g_count, 3) || '  ' || rpad(p_trigger, 26) || v_what);
    text_io.fclose(f);
  end log;
end trace;
