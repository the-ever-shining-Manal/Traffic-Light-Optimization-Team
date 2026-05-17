"""utils/plot.py — bar chart comparison of algorithm results.

Requires matplotlib. Install with:  pip install matplotlib
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


def plot_results(results: dict, save_path: str = "results.png") -> None:
    """Bar chart of avg wait, throughput, and cars passed per algorithm."""
    if not _HAS_MPL:
        print("[plot] matplotlib not installed – skipping chart.")
        return

    names   = list(results.keys())
    metrics = {
        "Avg wait (steps)":    [results[n]["average_wait"]          for n in names],
        "Throughput (cars/s)": [results[n].get("throughput", 0)     for n in names],
        "Cars passed":         [results[n]["cars_passed"]            for n in names],
    }

    colors = ["#E8593C", "#3B8BD4", "#1D9E75"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.patch.set_facecolor("#0f0f11")

    for ax, (title, vals), color in zip(axes, metrics.items(), colors):
        ax.set_facecolor("#1a1a1f")
        bars = ax.bar(names, vals, color=color, width=0.5, edgecolor="none")
        ax.set_title(title, color="#e8e6df", fontsize=11, pad=10)
        ax.tick_params(colors="#888")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333")
        # value labels on bars
        for bar, val in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02 * max(vals, default=1),
                f"{val:.2f}", ha="center", va="bottom",
                color="#e8e6df", fontsize=9,
            )

    fig.suptitle("Algorithm Benchmark", color="#e8e6df", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"[plot] saved -> {save_path}")
    plt.show()


def plot_statistical_report(agg: dict, save_path: str = "results_stats.png") -> None:
    """Mean ± 95 % CI bar chart from aggregate() output."""
    if not _HAS_MPL:
        print("[plot] matplotlib not installed – skipping chart.")
        return

    algo_names = list(agg.keys())
    metric     = "average_wait"
    means  = [agg[n][metric]["mean"] for n in algo_names]
    ci95s  = [agg[n][metric]["ci95"] for n in algo_names]

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#0f0f11")
    ax.set_facecolor("#1a1a1f")

    colors = ["#E8593C", "#3B8BD4", "#1D9E75"]
    bars = ax.bar(algo_names, means, yerr=ci95s, capsize=6,
                  color=colors[:len(algo_names)], width=0.5,
                  error_kw={"ecolor": "#aaa", "lw": 1.5})

    ax.set_ylabel("Average wait (steps)", color="#888")
    ax.set_title("Mean ± 95% CI  |  30 trials per algorithm",
                 color="#e8e6df", fontsize=12)
    ax.tick_params(colors="#888")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"[plot] saved -> {save_path}")
    plt.show()