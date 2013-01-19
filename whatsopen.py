#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def find_todays_hours(current_datetime, hourspecs):
    """ Returns a tuple of today's opening and closing times as time objects,
         or None if there are no hours specified for today. """

    # Save date and time separately for faster access.
    current_date, current_time = (current_datetime.date(),
                                  current_datetime.time())

    # The weekday and previous weekday,
    # using abbreviations that are used in the JSON.
    wdayabbrevs = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
    weekday = wdayabbrevs[current_datetime.weekday()]
    prevwday = wdayabbrevs[(current_datetime.weekday() + 6) % 7]

    for hourspec in hourspecs:
        try:
            opentime, closetime = (strtotime(hourspec[x])
              for x in ('open', 'close'))
        except KeyError:
            opentime, closetime = None, None

        # Skip this hourspec if it doesn't match current time.
        # This is tricky because of time ranges that overlap midnight!
        effd, effwday = current_date, weekday

        if opentime > closetime and current_time < closetime:
            # In this case, treat as if previous day.
            effwday = prevwday
            effd -= timedelta(1)

        # Check date range.
        if (('days' in hourspec and effwday not in hourspec['days'])
          or ('from' in hourspec and effd < strtodate(hourspec['from']))
          or ('to' in hourspec and effd > strtodate(hourspec['to']))):
            continue

        # Hourspec matches.
        return opentime, closetime

    # We fell through the loop, so no hourspec matched.
    return None, None


def is_time_between(t, start_time, end_time):
    """ Is the time t between start_time and end_time?
        If start_time > end_time, the range is assumed to span midnight. """
    if t > start_time and t < end_time:
        return True
    elif start_time > end_time and (t > start_time or t < end_time):
        return True
    else:
        return False


with open('hangouts.json') as fp:
    places = json.load(fp)['places']

for p in sorted(places.keys()):
    dt = datetime.today()
    opentime, closetime = find_todays_hours(dt, places[p])

    if opentime is not None:
        # Place has hours for today; check them.
        if is_time_between(dt.time(), opentime, closetime):
            # Bingo! Place is open.
            # Print place name.
            print p,

            # Space out to column 21.
            print ''.join([' ' for x in range(0, 20 - len(p))]),

            # Print closing time.
            str_closetime = re.sub('^(0)', ' ',
                                   closetime.strftime('%I:%M%P'))
            print 'until {}'.format(str_closetime)
