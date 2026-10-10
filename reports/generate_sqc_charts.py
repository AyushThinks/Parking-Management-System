"""Generate example Pareto and Fishbone diagrams for TQM discussion.

Replace the illustrative category counts with counts from your own defect checksheet
before submitting the charts as project evidence.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
EXAMPLE_COUNTS = {
    "Validation": 8,
    "Search / filter": 5,
    "Fee calculation": 4,
    "Slot allocation": 3,
    "CSV export": 2,
}

def make_pareto():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("Install matplotlib first: python -m pip install matplotlib") from exc
    items = sorted(EXAMPLE_COUNTS.items(), key=lambda item: item[1], reverse=True)
    labels = [item[0] for item in items]
    counts = [item[1] for item in items]
    total = sum(counts) or 1
    cumulative = []
    running = 0
    for count in counts:
        running += count
        cumulative.append(running / total * 100)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(labels, counts)
    ax.set_ylabel("Defect count (illustrative)")
    ax.set_title("Pareto Analysis — replace sample counts with observed data")
    ax.tick_params(axis="x", rotation=20)
    ax2 = ax.twinx()
    ax2.plot(labels, cumulative, marker="o")
    ax2.axhline(80, linestyle="--")
    ax2.set_ylabel("Cumulative percentage")
    ax2.set_ylim(0, 110)
    fig.tight_layout()
    fig.savefig(OUT / "pareto_chart.png", dpi=160)
    plt.close(fig)

def make_fishbone():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("Install matplotlib first: python -m pip install matplotlib") from exc
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    ax.annotate("", xy=(10.5, 4), xytext=(1, 4), arrowprops={"arrowstyle": "->", "linewidth": 2})
    ax.text(10.6, 4, "Parking defects", va="center", fontsize=12, weight="bold")
    causes = [
        (2.2, 6.5, "People", "Typing mistakes\nInsufficient training"),
        (4.5, 6.5, "Process", "Entry steps unclear\nFee rule misunderstood"),
        (6.8, 6.5, "Software", "Validation gap\nBoundary condition"),
        (2.2, 1.5, "Data", "Duplicate values\nIncorrect test data"),
        (4.5, 1.5, "Environment", "File permission\nDatabase locked"),
        (6.8, 1.5, "Measurement", "Incomplete checksheet\nUnverified counts"),
    ]
    for x, y, title, details in causes:
        top = y > 4
        ax.plot([x, x + 1.1], [y, 4], linewidth=1.5)
        ax.text(x, y + (0.15 if top else -0.25), title, weight="bold", ha="left")
        ax.text(x, y + (0.95 if top else -1.15), details, fontsize=8, va="center")
    ax.set_title("Fishbone / Ishikawa — potential cause categories to validate")
    fig.tight_layout()
    fig.savefig(OUT / "fishbone_diagram.png", dpi=160)
    plt.close(fig)

if __name__ == "__main__":
    make_pareto(); make_fishbone()
    print(f"Charts saved to {OUT}. Sample Pareto data is illustrative; replace it with actual counts.")
