import ast
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_parquet("hf://datasets/SAVSNET/PetEVAL/data/test-00000-of-00001.parquet")

def parce_text(label):
    if isinstance(label, str) and label.startswith("["):
        return ast.literal_eval(label)
    else:
        return label

dataset["icd_label"] = dataset["icd_label"].apply(parce_text)
ds_exploded = dataset.explode("icd_label").dropna(subset=["icd_label"])
disease_counts = ds_exploded["icd_label"].value_counts()

# draw chart
figure, axes = plt.subplots()
disease_counts.head(10)[::-1].plot(kind="barh", ax=axes)
axes.bar_label(axes.containers[0], padding=3)

plt.title("Top 10 Disease in PetEVAL dataset")
plt.xlabel("Count")
plt.show()
