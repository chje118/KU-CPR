import pandas as pd
from wsi_stats import main as wsi_main

# Path to pathology metadata
df_path = "path/to/pathology/data"
df_pathology = pd.read_excel(df_path)

# Path to WSI stats cache
df_wsi = wsi_main()

rekvnr_pathology = set(df_pathology["rekvnr"])
rekvnr_wsi = set(df_wsi["rekvnr"])

overlap = rekvnr_pathology & rekvnr_wsi
only_in_pathology = rekvnr_pathology - rekvnr_wsi
only_in_wsi = rekvnr_wsi - rekvnr_pathology

print(f"rekvnr in both: {len(overlap)}")
print(f"rekvnr only in pathology: {len(only_in_pathology)}")
print(f"rekvnr only in WSI: {len(only_in_wsi)}")

count_in_wsi = df_wsi["rekvnr"].isin(overlap).sum()
print(f"Number of rows in WSI with overlapping rekvnr: {count_in_wsi}")

counts_per_rekvnr = df_wsi[df_wsi["rekvnr"].isin(overlap)]["rekvnr"].value_counts()
print(counts_per_rekvnr)

if only_in_wsi:
    sample_rekvnr = next(iter(only_in_wsi))
    sample_row = df_wsi[df_wsi["rekvnr"] == sample_rekvnr].iloc[0]
    sample_path = sample_row.name
    print(f"Sample WSI file only in WSI: {sample_path}")
else:
    print("No rekvnr found only in WSI.")

# TODO: Explore metadata of WSIs only in WSI df
import openslide
if only_in_wsi:
    sample_rekvnr = next(iter(only_in_wsi))
    sample_row = df_wsi[df_wsi["rekvnr"] == sample_rekvnr].iloc[0]
    sample_path = sample_row.name
    print(f"Sample WSI file only in WSI: {sample_path}")

    slide = openslide.OpenSlide(sample_path)
    print("MRXS Metadata:")
    for key, value in slide.properties.items():
        print(f"{key}: {value}")
    slide.close()
else:
    print("No rekvnr found only in WSI.")


# Subset pathology DataFrame to only overlapping rekvnr
df_overlap = df_pathology[df_pathology["rekvnr"].isin(overlap)].copy()

# Count how many WSI files exist for each rekvnr
wsi_counts = df_wsi["rekvnr"].value_counts()

# Add the count as a new column in the pathology subset
df_overlap["wsi_count"] = df_overlap["rekvnr"].map(wsi_counts).fillna(0).astype(int)

# Create a mapping from rekvnr to list of filenames
filenames_per_rekvnr = df_wsi.groupby("rekvnr").apply(lambda g: list(g.index))

# Add the list of filenames as a new column in df_overlap
df_overlap["wsi_filenames"] = df_overlap["rekvnr"].map(filenames_per_rekvnr)

print(df_overlap[["rekvnr", "wsi_count", "wsi_filenames"]].head())

print(df_overlap.head())


# For overlapping rekvnr, count how many WSI files each has
wsi_per_rekvnr = df_wsi[df_wsi["rekvnr"].isin(overlap)]["rekvnr"].value_counts()

# Now count how many rekvnr have each possible WSI count
rekvnr_per_count = wsi_per_rekvnr.value_counts().sort_index()
print(rekvnr_per_count)



import seaborn as sns
import matplotlib.pyplot as plt

# Plot the distribution of WSI counts per rekvnr
plt.figure(figsize=(8, 5))
df_overlap["wsi_count"].value_counts().sort_index().plot(kind="bar")
plt.xlabel("Number of WSI per rekvnr")
plt.ylabel("Number of pathology cases")
plt.title("Distribution of WSI counts per rekvnr")
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_overlap,
    x="wsi_count",
    y="team",           # Change to "team" if your grouping column is named differently
    orient="h"
)
plt.xlabel("Number of WSI per rekvnr")
plt.ylabel("Team")
plt.title("Boxplot of WSI counts per rekvnr, grouped by team")
plt.tight_layout()
plt.show()