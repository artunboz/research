import json
from argparse import ArgumentParser

from tensorflow.python.framework.errors import OpError

from paths import DATA_DIR
from src.dimensionality_reduction.autoencoder.autoencoder_reducer import (
    AutoencoderReducer,
)
from src.dimensionality_reduction.autoencoder.deep_autoencoder import DeepAutoencoder

parser = ArgumentParser()
parser.add_argument("--feature-path", dest="feature_path")
args = parser.parse_args()

features_dir = f"{DATA_DIR}/{args.feature_path}"
reductions_dir = f"{features_dir}/reductions/deep_ae"

layer_dims_space = [[10], [50], [100], [200], [200, 100], [200, 50], [200, 10]]

with open(f"{features_dir}/feature_config.json", mode="r") as f:
    output_dim = json.load(f)["feature_dim"]

for i, layer_dims in enumerate(layer_dims_space):
    ae = DeepAutoencoder(layer_dims=layer_dims, output_dim=output_dim)
    reducer = AutoencoderReducer(ae, optimizer="adam", loss="mse")
    try:
        reducer.reduce_dimensions(features_dir=features_dir, epochs=30, batch_size=256)
    except OpError as e:
        print(f"TENSORFLOW EXCEPTION RAISE AT ITERATION {i}: {e}")
        continue
    reducer.save_reduced_features(f"{reductions_dir}/run_{i}")
    with open(f"{reductions_dir}/run_{i}/reducer_config.json", mode="r") as f:
        reducer_config = json.load(f)
    reducer_config["layer_dims"] = layer_dims
    with open(f"{reductions_dir}/run_{i}/reducer_config.json", mode="w") as f:
        json.dump(reducer_config, f)
