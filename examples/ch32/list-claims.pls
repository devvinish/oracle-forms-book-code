-- @where Trigger: WHEN-BUTTON-PRESSED on CTL.LIST
declare
  v_params  fjson.element_t := fjson.new_object(1);
  v_headers fjson.element_t := fjson.new_object(1);
  v_rheads  fjson.element_t;
  v_claims  fjson.element_t;
  v_claim   fjson.element_t;
  v_status  pls_integer;
begin
  fjson.put_string(v_params, 'mrn', :invoices.mrn);
  fjson.put_string(v_headers, 'Authorization', 'Bearer ' || :ctl.token);
  v_status := fhttp.issue_request('GET', 'http://localhost:8098',
                                  '/api/v1/claims?patient={mrn}', v_params, v_headers,
                                  null, null, '*', null, 5000, 5000, v_rheads, v_claims);
  go_block('CLAIMS');
  clear_block(no_validate);
  for i in 1 .. fjson.num_elements(v_claims) loop       -- the response is a JSON array
    v_claim := fjson.find(v_claims, i);
    :claims.claim_id := fjson.get_string_value(v_claim, 'claimId');
    :claims.invoice_id := fjson.get_number_value(v_claim, 'invoiceId');
    :claims.amount := fjson.get_number_value(v_claim, 'amount');
    :claims.approved := fjson.get_number_value(v_claim, 'approvedAmount');
    next_record;
  end loop;
  first_record;
  fjson.free_all;
end;
