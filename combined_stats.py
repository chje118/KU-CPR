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