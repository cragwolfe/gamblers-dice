#!/usr/bin/env python3.4
import os

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def record_result():
    "Write single line of data to file name"
    global fp
    json_payload = request.get_json()
    if not json_payload:
        return 'bad request: no json was posted', 400
    data = json_payload['data']
    nfields = 9
    if len(data.split(',')) != nfields:
        return 'bad request: expected %d fields' % nfields, 400
    if not data.endswith("\n"):
        data = data + "\n"
    fp.write(data)
    fp.flush()
    return 'got it', 200

if __name__ == '__main__':

    port = os.environ.get('DATA_COLLECTOR_PORT', '8777')
    data_file = os.environ.get('DATA_RESULTS_FILE', '/data/results.csv')

    global fp
    fp = open(data_file, 'w+')
    app.run(debug=True, host='0.0.0.0', port=int(port))
