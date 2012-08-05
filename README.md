# List open hangout spots

whatsopen.py tells you what's open:

    $ date
    Sat Aug  4 22:43:26 CDT 2012
    $ ./whatsopen.py
    Caffetto
    Hard Times Cafe
    Kitty Cat Klub

In this example, three late-night spots are open! Hangouts
and their hours are defined in hangouts.json. The app is
smart enough to correctly handle:

 * Varying hours by day of week
 * Summer hours (or any date range for which hours are
   different)
 * Places open past midnight (e.g., 4pm-2am)

Some limitations:

 * No geographical info / distance calculation
 * Doesn't warn you if place is "open", but closing in 5
   minutes
 * You have to manually edit a JSON file to change the data
   (hangouts.txt contains an idea for a friendlier format
   that is not yet used)

I wrote this to suggest places I can bring my laptop and
hack instead of sitting at home. The sample hangouts.json
file consists of cool wifi-enabled places near me in
Minneapolis, MN.
