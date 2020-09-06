"""Script to calculate median resolve time."""

import csv
from collections import namedtuple
from datetime import datetime

INC_DCT = {}
RESOLVE_TIMES_DCT = {}
RESOLVE_TIMES = []


def format_date(inc_datetime):
    """Formats dates."""
    date_fmt = '%Y-%m-%d %H:%M:%S'
    inc_datetime = datetime.strptime(inc_datetime, date_fmt)
    return inc_datetime


def open_csv(inc_file, dct):
    """Open csv and populate a dictionary with its contents."""
    with open(inc_file) as csv_file:
        f_csv = csv.reader(csv_file)
        column_headings = next(f_csv)
        csv_row = namedtuple('Row', column_headings)
        for rows in f_csv:
            row = csv_row(*rows)
            num = row.number
            opened = row.opened_at
            resolved = row.resolved_at
            dct[num] = opened, resolved


def output_median(a):
    """Print median resolve time in minutes."""
    print(f"Median: {a} minutes")


open_csv("incidents.csv", INC_DCT)

for inc_num, times in INC_DCT.items():
    if times[0] and times[1]:
        inc_open = format_date(times[0])
        inc_res = format_date(times[1])
        diff = inc_res - inc_open
        diff_mins = (diff.days * 24 * 60) + (diff.seconds/60)
        diff_mins_formatted = float("{:.2f}".format(diff_mins))
        RESOLVE_TIMES_DCT[inc_num] = diff_mins_formatted
        RESOLVE_TIMES.append(diff_mins_formatted)
    else:
        pass

print(f"Number of incidents: {len(RESOLVE_TIMES)}")

if len(RESOLVE_TIMES) % 2 == 0:
    NUM_TIMES = len(RESOLVE_TIMES)
    MED_1 = int(NUM_TIMES / 2)
    MED_2 = int(NUM_TIMES / 2 - 1)
    AVG = (RESOLVE_TIMES[MED_1] + RESOLVE_TIMES[MED_2]) / 2
    output_median(AVG)
else:
    NUM_TIMES = len(RESOLVE_TIMES)
    MED = int(NUM_TIMES / 2)
    output_median(RESOLVE_TIMES[MED])
