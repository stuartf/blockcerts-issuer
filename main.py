#!/usr/bin/python3
import json
import sys
from flask import Flask, request

import cert_issuer.config
from cert_issuer.blockchain_handlers import bitcoin
import cert_issuer.issue_certificates

app = Flask(__name__)
config = None

# Clear gunicorn's config out of our argv
sys.argv = [sys.argv[0]]


def get_config():
    global config
    if config is None:
        config = cert_issuer.config.get_config()
    return config


@app.route('/cert_issuer/api/v1.0/issue', methods=['POST'])
def issue():
    config = get_config()
    certificate_batch_handler, transaction_handler, connector = \
        bitcoin.instantiate_blockchain_handlers(config, False)
    certificate_batch_handler.set_certificates_in_batch(request.json)
    cert_issuer.issue_certificates.issue(config, certificate_batch_handler, transaction_handler)
    return json.dumps(certificate_batch_handler.proof)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
