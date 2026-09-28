from formkit import *
f = form('STEP0_REST', 'REST check')
main(f, 'Doctor from a REST service', 420, 200)
b = block(f, 'CTRL')
item(b, 'DOCTOR_ID', 'Doctor Id', 20, 40, 60, dt='number', length=6)
item(b, 'NAME', 'Name', 20, 90, 170, kind='display')
item(b, 'SPECIALTY', 'Specialty', 200, 90, 120, kind='display')
item(b, 'FEE', 'Fee (USD)', 330, 90, 60, dt='number', kind='display')
btn = item(b, 'FETCH', 'Fetch', 100, 38, 70, 20, kind='button')
trigger(btn, 'WHEN-BUTTON-PRESSED', """
declare
  l_status  pls_integer;
  l_headers fjson.element_t;
  l_doctor  fjson.element_t;
begin
  l_status := fhttp.issue_request(
                method           => 'GET',
                server_url_or_id => 'http://localhost:8099',
                uri_template     => '/api/doctor-{id}.json',
                url_parameters   => fjson.parse('{"id":"' || :ctrl.doctor_id || '"}'),
                request_headers  => null,
                request_body     => null,
                accept           => null,
                parse            => '*',
                authorization_info => null,
                connect_timeout  => 10000,
                read_timeout     => 10000,
                response_headers => l_headers,
                response_body    => l_doctor);
  :ctrl.name      := fjson.get_string_value(l_doctor, 'name');
  :ctrl.specialty := fjson.get_string_value(l_doctor, 'specialty');
  :ctrl.fee       := fjson.get_number_value(l_doctor, 'feeUsd');
  message('HTTP status ' || l_status);
end;
""")
save(f)
