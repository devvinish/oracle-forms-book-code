-- @where Trigger: WHEN-NEW-FORM-INSTANCE (form CH31_FBEAN)
begin
  fbean.register_bean('CTL.PROGRESS', 1, 'javax.swing.JProgressBar');  -- any JavaBean
  fbean.invoke('CTL.PROGRESS', 1, 'setMaximum', 100);
  fbean.set_property('CTL.PROGRESS', 1, 'StringPainted', 'true');     -- setStringPainted
end;
