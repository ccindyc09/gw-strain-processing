# GW Strain Processing (O1–O4)

This repository contains Python scripts used to download and process gravitational-wave strain data from the GWOSC public database.

## Contents

### Event Lists
- events_01.txt → O1 events
- events_02.txt → O2 events
- events_03.txt → O3 events
- events_04.txt → O4 events

### Scripts

make_gps_table.py  
→ Generates table of event names and GPS merger times

extract_time_power_arrays.py  
→ Downloads strain data and extracts time + power arrays around merger

plot_event_strain.py  
→ Produces strain vs time visualization around peak merger

### Output
events_all_gps.csv  
→ Combined list of events with GPS merger times

## Data Source
Gravitational Wave Open Science Center (GWOSC)

Data accessed using:
- GWpy
- gwosc Python library
