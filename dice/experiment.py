#!/usr/bin/env python3.4
from datetime import datetime
import math
import os
import sys

import requests

from gamblersdice import GenericDie

class state():
    pass

def header():
    """Header for easy-to-read result."""
    return ("%-6s %-15s %9s               %s" %
            ('Bias',
             'Number of rolls',
             'Normalized freq stddev',
             'Frequencies')
           )

def format_result(the_die):
    """Easy-to-read result."""
    return ("%-6s %15d %6.3f              %s" %
            (the_die.bias,
             the_die.n,
             the_die.freq_std * math.sqrt(the_die.n),
             str(the_die.freq)
            )
           )

def format_csv_result(the_die):
    """Comma separated row: 
         bias, total_rolls, normalized_freq_std_dev,
         roll_1_freq, ... , roll_n_freq
    """
    result = [the_die.bias,
              str(the_die.n),
              str(the_die.freq_std * math.sqrt(the_die.n))]
    result.extend(['%0.18f' % f for f in the_die.freq])
    return ",".join(result)

def post_result(the_die, port):
    """Post one result as csv line to data collector."""
    record = format_csv_result(the_die)
    hostname = os.environ.get('DATA_COLLECTOR_HOSTNAME',
                              'localhost')
    r = requests.post('http://%s:%s' % (hostname, port),
                      json={'data':record})
    if r.status_code != 200:
        raise RuntimeError("Error posting to data collector: "+r.text)

if __name__ == '__main__':
    die_bias = os.environ.get('DIE_BIAS', 'random')
    seconds_threshold = int(os.environ.get('SOFT_STOP_SECONDS', '3000'))
    iters_for_first_result = os.environ.get('FIRST_ITER_TO_RECORD', 10)
    num_sides = os.environ.get('SIDES_ON_DIE', 6)
    data_collector_port = os.environ.get('DATA_COLLECTOR_PORT', '8777')


    the_die = GenericDie(sides=num_sides, bias=die_bias)

    state = state()
    state.begin_time = datetime.now()
    state.next_recording = iters_for_first_result
    state.iters = 0

    def _maybe_record_result():
        if state.iters != state.next_recording:
            return
        state.next_recording = state.iters * 2
        print(format_result(the_die), flush=True)
        post_result(the_die, data_collector_port)

        now = datetime.now()
        if (now - state.begin_time).total_seconds() > seconds_threshold:
            sys.exit(0)

    print("Beginning experiment for %s die" % the_die.bias)
    print(header(), flush=True)
    while True:
        the_die.roll()
        state.iters += 1
        _maybe_record_result()
