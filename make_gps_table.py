import csv
from gwosc import datasets

RUN_FILES = {
    "O1": "events_01.txt",
    "O2": "events_02.txt",
    "O3": "events_03.txt",
    "O4": "events_04.txt",
}

with open("events_all_gps.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["run", "event", "gps"])
    for run, fname in RUN_FILES.items():
        with open(fname, "r") as fin:
            events = [line.strip() for line in fin if line.strip()]
        for ev in events:
            try:
                w.writerow([run, ev, datasets.event_gps(ev)])
            except Exception:
                w.writerow([run, ev, "ERROR"])
