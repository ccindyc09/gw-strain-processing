from gwpy.timeseries import TimeSeries
from gwosc import datasets
import numpy as np
import os

RUN_FILES = {
    "O1": "events_01.txt",
    "O2": "events_02.txt",
    "O3": "events_03.txt",
    "O4": "events_04.txt",
}

def compute_time_strain_power(
    event_name,
    det="H1",
    pad=8.0,
    fs=4096,
    band=(35, 350),
    fftlength=4.0,
    peak_window=3.0,
):
    gps = datasets.event_gps(event_name)

    ts = TimeSeries.fetch_open_data(
        det,
        gps - pad,
        gps + pad,
        sample_rate=fs,
        cache=False
    )

    ts = ts.bandpass(*band)
    ts = ts.detrend("constant")
    ts = ts.whiten(fftlength=fftlength)

    ts = ts.crop(gps - pad + 1.0, gps + pad - 1.0)

    y = ts.value.astype(float)
    peak_idx = np.argmax(np.abs(y))
    t_peak = ts.times.value[peak_idx]

    t_rel_full = ts.times.value - t_peak
    sel = (t_rel_full >= -peak_window) & (t_rel_full <= peak_window)

    t_rel = t_rel_full[sel].astype(np.float32)
    strain = y[sel].astype(np.float32)
    power = (strain ** 2).astype(np.float32)

    return t_rel, strain, power


if __name__ == "__main__":
    for RUN, event_file in RUN_FILES.items():
        if not os.path.exists(event_file):
            print(f"[SKIP RUN] {RUN}: missing file {event_file}")
            continue

        with open(event_file, "r") as f:
            EVENTS = [line.strip() for line in f if line.strip()]

        OUT_DIR = os.path.join("arrays_power", RUN)
        os.makedirs(OUT_DIR, exist_ok=True)

        print(f"\n=== Processing {RUN} ({len(EVENTS)} events) ===")

        for event in EVENTS:
            try:
                event_dir = os.path.join(OUT_DIR, event)
                os.makedirs(event_dir, exist_ok=True)

                t, s, p = compute_time_strain_power(event)

                np.save(os.path.join(event_dir, "H1_time.npy"), t)
                np.save(os.path.join(event_dir, "H1_strain.npy"), s)
                np.save(os.path.join(event_dir, "H1_power.npy"), p)

                print(f"Saved {RUN} {event} ({len(t)} samples)")

            except Exception as e:
                print(f"[SKIP] {RUN} {event}: {type(e).__name__} — {e}")
