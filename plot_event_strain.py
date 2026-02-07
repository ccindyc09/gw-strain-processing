from gwpy.timeseries import TimeSeries
from gwosc import datasets
import matplotlib.pyplot as plt
import numpy as np


def plot_ligo_style_strain_only(
    event_name="GW150914",
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

    peak_idx = np.argmax(np.abs(ts.value))

    t_peak = ts.times.value[peak_idx]

    t_rel = ts.times.value - t_peak

    sel = (t_rel >= -peak_window) & (t_rel <= peak_window)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(t_rel[sel], ts.value[sel], lw=1.1, label=f"{det} whitened")
    ax.axvline(0, ls="--", color="r", alpha=0.8, label="Peak strain")

    ax.set_xlim(-peak_window, peak_window)
    ax.set_xlabel("Time relative to peak (s)")
    ax.set_ylabel("Strain (whitened)")
    ax.set_title(f"{event_name} ({det}) — Strain vs Time (±3 s around peak)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()

    out = f"{event_name}_{det}_strain_peak_3s.png"
    fig.savefig(out, dpi=150)
    print(f"Saved → {out}")

    plt.show()


if __name__ == "__main__":
    plot_ligo_style_strain_only(
        event_name="GW150914",
        det="H1",
        pad=8.0,
        band=(35, 350),
        fftlength=4.0,
        peak_window=3.0,
    )


# check event ids (focus on binary inspire module- confirmed event), make a list of event ids- excel file, store arrays
# get proper plot, validate signal first
# -4.5-3
# proper reference, explain each line
# excel-hdf files
# store files with multiple plots, geat a list of it as well- make sure to get reference
# get csv files, store the arrays, 104 in total of all O

# define peak - 3 second before and after peak, not 0
# store arrays into .npy, 1 dimension for time, and one for power