#!/usr/libexec/platform-python
"""A small insurance-claims REST service for Chapter 32 (Python standard library only).
   GET  /api/v1/plans/{id}              the plan's coverage              (no authorization)
   POST /api/v1/claims                  submit a claim   (Authorization: Bearer cw-lab-token)
   GET  /api/v1/claims?patient={mrn}    the patient's claims             (Authorization)
Claims are kept in claims.json next to this script; delete it to start again. Port 8098.
   Run it with any Python 3: python3 claims_api.py"""
import json, os, re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

TOKEN = 'cw-lab-token'
STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claims.json')
PLANS = {1: ('Star Health', 'Family Floater', 80, 500000), 2: ('Star Health', 'Senior Care', 70, 300000),
         3: ('HDFC Ergo', 'Optima Secure', 90, 1000000), 4: ('Niva Bupa', 'ReAssure', 85, 500000),
         5: ('ICICI Lombard', 'Complete Health', 75, 500000), 6: ('Care Health', 'Care Supreme', 80, 700000)}

def load():
    return json.load(open(STORE)) if os.path.exists(STORE) else []

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_body(self):                        # FHTTP sends bodies with chunked transfer encoding
        if 'chunked' in self.headers.get('Transfer-Encoding', '').lower():
            data = b''
            while True:
                size = int(self.rfile.readline().split(b';')[0], 16)
                if size == 0:
                    self.rfile.readline()
                    return data
                data += self.rfile.read(size)
                self.rfile.readline()
        return self.rfile.read(int(self.headers.get('Content-Length', 0)))

    def authorized(self):
        if self.headers.get('Authorization') != 'Bearer ' + TOKEN:
            self.reply(401, {'error': 'missing or invalid bearer token'})
            return False
        return True

    def do_GET(self):
        url = urlparse(self.path)
        m = re.match(r'^/api/v1/plans/(\d+)$', url.path)
        if m:
            p = PLANS.get(int(m.group(1)))
            if not p:
                return self.reply(404, {'error': 'no plan ' + m.group(1)})
            return self.reply(200, {'planId': int(m.group(1)), 'provider': p[0], 'planName': p[1],
                                    'coveragePct': p[2], 'annualLimit': p[3]})
        if url.path == '/api/v1/claims':
            if not self.authorized():
                return
            mrn = parse_qs(url.query).get('patient', [''])[0]
            return self.reply(200, [c for c in load() if c['patientMrn'] == mrn])
        self.reply(404, {'error': 'unknown resource ' + url.path})

    def do_POST(self):
        if urlparse(self.path).path != '/api/v1/claims':
            return self.reply(404, {'error': 'unknown resource'})
        if not self.authorized():
            return
        raw = self.read_body()
        open(os.path.join(os.path.dirname(STORE), 'claims_api.log'), 'a').write('  headers %s\n  body %s\n' % (dict(self.headers), raw.decode()))
        body = json.loads(raw or b'{}')
        plan = PLANS.get(body.get('planId'))
        if not plan or not body.get('amount') or body['amount'] <= 0:
            return self.reply(422, {'error': 'planId and a positive amount are required'})
        claims = load()
        claim = {'claimId': 'CLM-2026-%06d' % (101 + len(claims)), 'status': 'RECEIVED',
                 'patientMrn': body.get('patientMrn'), 'invoiceId': body.get('invoiceId'),
                 'amount': body['amount'], 'approvedAmount': round(body['amount'] * plan[2] / 100, 2)}
        claims.append(claim)
        json.dump(claims, open(STORE, 'w'), indent=1)
        self.reply(201, claim)

    def log_message(self, fmt, *args):
        open(os.path.join(os.path.dirname(STORE), 'claims_api.log'), 'a').write('%s %s\n' % (self.command, self.path))

HTTPServer(('0.0.0.0', 8098), Handler).serve_forever()
