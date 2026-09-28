-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.COVERAGE
declare
  v_params  fjson.element_t := fjson.new_object(1);
  v_headers fjson.element_t;
  v_plan    fjson.element_t;
  v_status  pls_integer;
begin
  fjson.put_string(v_params, 'id', to_char(:invoices.plan_id));
  v_status := fhttp.issue_request(
                method             => 'GET',
                server_url_or_id   => 'http://localhost:8098',
                uri_template       => '/api/v1/plans/{id}',
                url_parameters     => v_params,
                request_headers    => null,
                request_body       => null,
                accept             => null,
                parse              => '*',
                authorization_info => null,
                connect_timeout    => 5000,
                read_timeout       => 5000,
                response_headers   => v_headers,
                response_body      => v_plan);
  :ctl.plan := fjson.get_string_value(v_plan, 'provider') || ', '
               || fjson.get_string_value(v_plan, 'planName') || ': '
               || fjson.get_number_value(v_plan, 'coveragePct') || '%';
  :ctl.covered := round(:invoices.total_amount
                        * fjson.get_number_value(v_plan, 'coveragePct') / 100, 2);
  fjson.free_all;                                         -- release the parsed JSON
end;
