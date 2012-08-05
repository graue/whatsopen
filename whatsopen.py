#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Show time when an open place will close, or vice versa.
# Also: parse hangouts.txt. Better than handwriting JSON.

from datetime import datetime, time, timedelta
import re
try:
    import simplejson as json
except ImportError:
    import json


def strtodate(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def strtotime(s):
    m = re.match("(\d+):(\d+)(a|p)m?$", s)
    if m is not None:
        hour = 0 if m.group(1) == '12' else int(m.group(1))
        return time(hour + (12 if m.group(3) == 'p' else 0),
            int(m.group(2)))
    m = re.match("(\d+)(a|p)m?$", s)
    hour = 0 if m.group(1) == '12' else int(m.group(1))
    return time(hour + (12 if m.group(2) == 'p' else 0))


def placeopen(hourspecs, dt):
    d, t = dt.date(), dt.time()
    wdayabbrevs = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
    weekday = wdayabbrevs[dt.weekday()]
    prevwday = wdayabbrevs[(dt.weekday() + 6) % 7]

    for hourspec in hourspecs:
        try:
            opentime, closetime = (strtotime(hourspec[x]) \
              for x in ('open', 'close'))
        except KeyError:
            opentime, closetime = None, None

        # Skip this hourspec if it doesn't match current time.
        # This is tricky because of time ranges that overlap midnight!
        effd, effwday = d, weekday

        if opentime > closetime and t < closetime:
            # In this case, treat as if previous day.
            effwday = prevwday
            effd -= timedelta(1)

        # Check date range.
        if (('days' in hourspec and effwday not in hourspec['days'])
          or ('from' in hourspec and effd < strtodate(hourspec['from']))
          or ('to' in hourspec and effd > strtodate(hourspec['to']))):
            continue

        # Hourspec matches — compare with current time.
        if t > opentime and t < closetime:
            return True
        elif opentime > closetime and (t > opentime or t < closetime):
            return True
        else:
            return False

    # No hourspec matched, assume closed.
    return False


with open('hangouts.json') as fp:
    places = json.load(fp)['places']

for p in sorted(places.keys()):
    status = 'open' if placeopen(places[p], datetime.today()) else 'closed'
    if status == 'open':
        print p
