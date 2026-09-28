-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.SUBMIT
declare
  v_headers  fjson.element_t := fjson.new_object(1);
  v_body     fjson.element_t := fjson.new_object(4);
  v_response fjson.element_t;
  v_rheaders fjson.element_t;
  v_status   pls_integer;
begin
  fjson.put_string(v_headers, 'Authorization', 'Bearer ' || :ctl.token);
  fjson.put_string(v_body, 'patientMrn', :invoices.mrn);
  fjson.put_number(v_body, 'invoiceId', :invoices.invoice_id);
  fjson.put_number(v_body, 'planId', :invoices.plan_id);
  fjson.put_number(v_body, 'amount', :invoices.total_amount);
  v_status := fhttp.issue_request(
                method             => 'POST',
                server_url_or_id   => 'http://localhost:8098',
                uri_template       => '/api/v1/claims',
                url_parameters     => null,
                request_headers    => v_headers,
                request_body       => v_body,
                accept             => '401,422',             -- handled below
                parse              => '*',
                authorization_info => null,
                connect_timeout    => 5000,
                read_timeout       => 5000,
                response_headers   => v_rheaders,
                response_body      => v_response);
  if v_status = 201 then
    :ctl.result := 'Claim ' || fjson.get_string_value(v_response, 'claimId') || ' '
                   || fjson.get_string_value(v_response, 'status') || ', approved '
                   || fjson.get_number_value(v_response, 'approvedAmount');
  else
    :ctl.result := 'HTTP ' || v_status || ': '
                   || fjson.get_string_value(v_response, 'error');
  end if;
  fjson.free_all;
end;
