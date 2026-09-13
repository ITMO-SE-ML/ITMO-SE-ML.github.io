"""Reproducible EDA figures for Lecture 1.

Dataset: UCI Wine, distributed with scikit-learn.
Run: python eda_wine.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_wine


OUT = Path(__file__).resolve().parent / "assets" / "wine_eda"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#202124"
BLUE = "#3159B8"
CORAL = "#D65443"
OCHRE = "#D59A2A"
GREEN = "#4E7B62"
PAPER = "#FAF9F6"
PALETTE = [BLUE, CORAL, OCHRE]

sns.set_theme(
    style="whitegrid",
    context="talk",
    font="DejaVu Sans",
    rc={
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "axes.edgecolor": "#D9D7D1",
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "grid.color": "#E8E5DE",
        "grid.linewidth": 0.8,
    },
)

wine = load_wine(as_frame=True)
df = wine.frame.rename(columns={"target": "class"})
df["class"] = df["class"].map({0: "class 1", 1: "class 2", 2: "class 3"})


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


# 1. Two complementary views of one feature: histogram + ECDF.
fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
sns.histplot(
    data=df,
    x="alcohol",
    hue="class",
    bins=15,
    element="step",
    stat="density",
    common_norm=False,
    palette=PALETTE,
    alpha=0.18,
    linewidth=2,
    ax=axes[0],
)
axes[0].set_title("Распределение alcohol")
axes[0].set_xlabel("Alcohol")
axes[0].set_ylabel("Плотность")

sns.ecdfplot(
    data=df,
    x="alcohol",
    hue="class",
    palette=PALETTE,
    linewidth=2.4,
    ax=axes[1],
)
axes[1].set_title("Эмпирическая функция распределения")
axes[1].set_xlabel("Alcohol")
axes[1].set_ylabel("Доля наблюдений ≤ x")
for ax in axes:
    sns.despine(ax=ax)
fig.tight_layout()
save(fig, "wine_distributions.png")


# 2. Class balance and a feature comparison across classes.
fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), gridspec_kw={"width_ratios": [0.8, 1.5]})
counts = df["class"].value_counts().sort_index()
axes[0].bar(counts.index, counts.values, color=PALETTE, width=0.66)
axes[0].set_title("Баланс классов")
axes[0].set_xlabel("")
axes[0].set_ylabel("Число объектов")
for i, value in enumerate(counts.values):
    axes[0].text(i, value + 1.5, str(value), ha="center", va="bottom", fontsize=13, weight="bold")
axes[0].set_ylim(0, max(counts.values) * 1.18)

sns.boxplot(
    data=df,
    x="class",
    y="proline",
    hue="class",
    palette=PALETTE,
    width=0.58,
    linewidth=1.4,
    legend=False,
    ax=axes[1],
)
sns.stripplot(
    data=df,
    x="class",
    y="proline",
    color=INK,
    alpha=0.28,
    size=3,
    jitter=0.18,
    ax=axes[1],
)
axes[1].set_title("Proline различается между классами")
axes[1].set_xlabel("")
axes[1].set_ylabel("Proline")
for ax in axes:
    sns.despine(ax=ax)
fig.tight_layout()
save(fig, "wine_groups.png")


# 3. Pairwise relationship and a compact correlation map.
fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.0), gridspec_kw={"width_ratios": [1.0, 1.15]})
sns.scatterplot(
    data=df,
    x="flavanoids",
    y="color_intensity",
    hue="class",
    palette=PALETTE,
    s=66,
    alpha=0.82,
    edgecolor="white",
    linewidth=0.7,
    ax=axes[0],
)
axes[0].set_title("Связь двух признаков")
axes[0].set_xlabel("Flavanoids")
axes[0].set_ylabel("Color intensity")
axes[0].legend(title="", frameon=False, loc="upper right")

features = ["alcohol", "malic_acid", "total_phenols", "flavanoids", "color_intensity", "proline"]
corr = df[features].corr()
sns.heatmap(
    corr,
    vmin=-1,
    vmax=1,
    center=0,
    cmap=sns.diverging_palette(230, 15, as_cmap=True),
    square=True,
    linewidths=0.7,
    linecolor=PAPER,
    annot=True,
    fmt=".2f",
    annot_kws={"fontsize": 10},
    cbar_kws={"shrink": 0.72, "label": "Корреляция"},
    ax=axes[1],
)
axes[1].set_title("Корреляции признаков")
axes[1].tick_params(axis="x", rotation=45, labelsize=9)
axes[1].tick_params(axis="y", rotation=0, labelsize=9)
fig.tight_layout()
save(fig, "wine_relationships.png")


# 4. Outliers by the 1.5 IQR rule for selected features.
features = ["malic_acid", "ash", "magnesium", "color_intensity", "proline"]
long = df[features].apply(lambda s: (s - s.median()) / s.std()).melt(
    var_name="feature", value_name="robust_view"
)
q1 = df[features].quantile(0.25)
q3 = df[features].quantile(0.75)
iqr = q3 - q1
outlier_counts = ((df[features] < (q1 - 1.5 * iqr)) | (df[features] > (q3 + 1.5 * iqr))).sum()

fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), gridspec_kw={"width_ratios": [1.35, 0.8]})
sns.boxplot(
    data=long,
    x="feature",
    y="robust_view",
    color="#BFCBE8",
    width=0.62,
    linewidth=1.4,
    fliersize=4,
    ax=axes[0],
)
axes[0].axhline(0, color=INK, linewidth=0.9, alpha=0.55)
axes[0].set_title("Выбросы видны после приведения масштаба")
axes[0].set_xlabel("")
axes[0].set_ylabel("(x − median) / std")
axes[0].tick_params(axis="x", rotation=24, labelsize=10)

axes[1].barh(outlier_counts.index, outlier_counts.values, color=CORAL, alpha=0.9)
axes[1].set_title("Число выбросов по 1.5 IQR")
axes[1].set_xlabel("Объекты")
axes[1].set_ylabel("")
axes[1].invert_yaxis()
for y, value in enumerate(outlier_counts.values):
    axes[1].text(value + 0.25, y, str(int(value)), va="center", fontsize=12, weight="bold")
axes[1].set_xlim(0, max(outlier_counts.values) + 3)
for ax in axes:
    sns.despine(ax=ax)
fig.tight_layout()
save(fig, "wine_outliers.png")


# Machine-readable summary used in the lecture source.
summary = {
    "rows": int(df.shape[0]),
    "numeric_features": int(df.select_dtypes(include=np.number).shape[1]),
    "classes": int(df["class"].nunique()),
    "missing_values": int(df.isna().sum().sum()),
    "duplicate_rows": int(df.duplicated().sum()),
    "alcohol_mean": float(df["alcohol"].mean()),
    "alcohol_median": float(df["alcohol"].median()),
}
pd.Series(summary).to_json(OUT / "wine_summary.json", force_ascii=False, indent=2)
print(pd.Series(summary).to_string())
