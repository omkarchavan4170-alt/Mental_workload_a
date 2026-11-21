
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("graphs", exist_ok=True)

df = pd.read_csv("results/subject_results.csv")

models = df["Model"].unique()

# Arrange results into model-wise tables
accuracy = df.pivot_table(
    index="Subject",
    columns="Model",
    values="Accuracy"
)

metrics = df.groupby("Model")[
    ["Accuracy", "Precision", "Recall", "F1"]
].mean().reindex(models)

# ------------------------------------------------
# 1. MEAN ACCURACY COMPARISON
# ------------------------------------------------

mean_acc = df.groupby("Model")["Accuracy"].mean()
std_acc = df.groupby("Model")["Accuracy"].std()

plt.figure(figsize=(9, 5))

plt.bar(
    mean_acc.index,
    mean_acc.values,
    yerr=std_acc.values,
    capsize=5
)

plt.ylabel("Accuracy (%)")
plt.xlabel("Model Architecture")
plt.title("Mean LOSO Accuracy Comparison")
plt.ylim(0, 105)
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("graphs/accuracy_comparison.png", dpi=300)
plt.show()


# ------------------------------------------------
# 2. ACCURACY DISTRIBUTION (BOXPLOT)
# ------------------------------------------------

plt.figure(figsize=(9, 5))

data = [
    df[df["Model"] == model]["Accuracy"].values
    for model in models
]

plt.boxplot(data, tick_labels=models)

plt.ylabel("Accuracy (%)")
plt.xlabel("Model Architecture")
plt.title("Subject-wise Accuracy Distribution")
plt.ylim(0, 105)
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("graphs/accuracy_boxplot.png", dpi=300)
plt.show()


# ------------------------------------------------
# 3. SUBJECT-WISE ACCURACY COMPARISON
# ------------------------------------------------

plt.figure(figsize=(13, 6))

for model in models:

    plt.plot(
        accuracy.index,
        accuracy[model],
        marker="o",
        markersize=3,
        label=model
    )

plt.xlabel("Subject ID")
plt.ylabel("Accuracy (%)")
plt.title("LOSO Subject-wise Performance")
plt.ylim(0, 105)
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("graphs/subject_accuracy.png", dpi=300)
plt.show()


# ------------------------------------------------
# 4. PRECISION, RECALL AND F1 COMPARISON
# ------------------------------------------------

metrics[["Precision", "Recall", "F1"]].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.ylabel("Score (%)")
plt.xlabel("Model Architecture")
plt.title("Precision, Recall and F1 Comparison")
plt.ylim(0, 105)
plt.xticks(rotation=20)
plt.legend()
plt.tight_layout()

plt.savefig("graphs/classification_metrics.png", dpi=300)
plt.show()


# ------------------------------------------------
# 5. PRINT SUMMARY
# ------------------------------------------------

print("\nMODEL PERFORMANCE SUMMARY")

print(
    df.groupby("Model")[
        ["Accuracy", "Precision", "Recall", "F1"]
    ].mean().round(2)
)

print("\nAll graphs saved in ./graphs/")
