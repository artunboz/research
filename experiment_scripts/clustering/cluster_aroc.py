import os
from argparse import ArgumentParser

from tqdm.contrib.itertools import product

from paths import DATA_DIR
from src.clustering.aroc.aroc_clustering import AROClustering

parser = ArgumentParser()
parser.add_argument("--feature-path", dest="feature_path")
args = parser.parse_args()

feature_folder_path = f"{DATA_DIR}/{args.feature_path}"
aroc_folder_path = f"{feature_folder_path}/clustering/aroc"
os.makedirs(aroc_folder_path)

n_neighbours_space = [190, 200, 210]
threshold_space = [0.08, 0.1, 0.12]
min_samples_space = [10, 100]

for i, (n_neighbours, threshold, min_samples) in enumerate(
    product(n_neighbours_space, threshold_space, min_samples_space)
):
    clustering = AROClustering(
        n_neighbours=n_neighbours, threshold=threshold, min_samples=min_samples
    )
    clustering.cluster(feature_folder_path)
    clustering.save_cluster_labels(f"{aroc_folder_path}/run_{i}")
