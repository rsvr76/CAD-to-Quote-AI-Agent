"""Analyze water level ranges and find the 12 orphan nodes."""
import os
import numpy as np
import pandas as pd

BASE = r"d:\Hackathon\Kaggle\UrbanFloodBench\Given\Datasets\Updated datasets\Models"
SUB_PATH = r"d:\Hackathon\Kaggle\UrbanFloodBench\Given\Datasets\Former dataset\urban-flood-modelling\sample_submission.csv"

# 1. Check elevation ranges from static data
print("=" * 60)
print("ELEVATION RANGES FROM STATIC DATA")
print("=" * 60)
for mid in [1, 2]:
    for split in ["train", "test"]:
        d = os.path.join(BASE, f"model_{mid}", split)
        sf_2d = pd.read_csv(os.path.join(d, "2d_node_static.csv"))
        sf_1d = pd.read_csv(os.path.join(d, "1d_node_static.csv"))
        print(f"\nModel {mid} ({split}):")
        print(f"  1D nodes: {len(sf_1d)}, node_idx range: [{sf_1d['node_idx'].min()}, {sf_1d['node_idx'].max()}]")
        print(f"  1D invert_elevation: [{sf_1d['invert_elevation'].min():.2f}, {sf_1d['invert_elevation'].max():.2f}]")
        print(f"  2D nodes: {len(sf_2d)}, node_idx range: [{sf_2d['node_idx'].min()}, {sf_2d['node_idx'].max()}]")
        print(f"  2D min_elevation: [{sf_2d['min_elevation'].min():.2f}, {sf_2d['min_elevation'].max():.2f}]")
        print(f"  2D elevation: [{sf_2d['elevation'].min():.2f}, {sf_2d['elevation'].max():.2f}]")

# 2. Find the 12 orphan nodes
print("\n" + "=" * 60)
print("FINDING ORPHAN NODES")
print("=" * 60)
sub = pd.read_csv(SUB_PATH)
print(f"Submission rows: {len(sub):,}")

for mid in [1, 2]:
    d_test = os.path.join(BASE, f"model_{mid}", "test")
    sf_2d = pd.read_csv(os.path.join(d_test, "2d_node_static.csv"))
    sf_1d = pd.read_csv(os.path.join(d_test, "1d_node_static.csv"))
    
    static_1d_ids = set(sf_1d["node_idx"].values)
    static_2d_ids = set(sf_2d["node_idx"].values)
    
    sub_m = sub[sub["model_id"] == mid]
    sub_1d = sub_m[sub_m["node_type"] == 1]["node_id"].unique()
    sub_2d = sub_m[sub_m["node_type"] == 2]["node_id"].unique()
    
    orphan_1d = set(sub_1d) - static_1d_ids
    orphan_2d = set(sub_2d) - static_2d_ids
    
    print(f"\nModel {mid}:")
    print(f"  Submission 1D node_ids: {len(sub_1d)}, Static: {len(static_1d_ids)}, Orphans: {orphan_1d}")
    print(f"  Submission 2D node_ids: {len(sub_2d)}, Static: {len(static_2d_ids)}, Orphans: {orphan_2d}")

# 3. Analyze actual WL ranges from training events
print("\n" + "=" * 60)
print("WATER LEVEL RANGES FROM TRAINING DATA")
print("=" * 60)
for mid in [1, 2]:
    d_train = os.path.join(BASE, f"model_{mid}", "train")
    events = sorted([int(x.replace("event_", "")) for x in os.listdir(d_train)
                     if x.startswith("event_")])
    
    wl_min_1d = float('inf')
    wl_max_1d = float('-inf')
    wl_min_2d = float('inf')
    wl_max_2d = float('-inf')
    
    for eid in events[:10]:  # Sample first 10 events
        ed = os.path.join(d_train, f"event_{eid}")
        wl1 = pd.read_csv(os.path.join(ed, "1d_node_waterlevel.csv")).values[:, 1:]
        wl2 = pd.read_csv(os.path.join(ed, "2d_node_waterlevel.csv")).values[:, 1:]
        
        wl_min_1d = min(wl_min_1d, np.nanmin(wl1))
        wl_max_1d = max(wl_max_1d, np.nanmax(wl1))
        wl_min_2d = min(wl_min_2d, np.nanmin(wl2))
        wl_max_2d = max(wl_max_2d, np.nanmax(wl2))
    
    print(f"\nModel {mid} (first 10 events):")
    print(f"  1D WL range: [{wl_min_1d:.4f}, {wl_max_1d:.4f}]")
    print(f"  2D WL range: [{wl_min_2d:.4f}, {wl_max_2d:.4f}]")
    
    # Check ceiling: what is floor+15 max?
    d_test = os.path.join(BASE, f"model_{mid}", "test")
    sf_2d = pd.read_csv(os.path.join(d_test, "2d_node_static.csv"))
    max_ceiling = sf_2d["min_elevation"].max() + 15.0
    print(f"  Max possible ceiling (min_elev+15): {max_ceiling:.4f}")

print("\nDone!")
