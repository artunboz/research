from itertools import product

from paths import DATA_DIR
from src.features.global_features.lbp_feature import LBPFeature

image_folder_path = f"{DATA_DIR}/deneme"

resize_size_space = [(48, 48), (96, 96)]
p_space = [8, 16, 24]
r_space = [1, 2, 3]
method_space = ["default", "ror", "uniform"]

for i, (resize_size, p, r, method) in enumerate(
    product(resize_size_space, p_space, r_space, method_space)
):
    lbp = LBPFeature(resize_size=resize_size, p=p, r=r, method=method)
    lbp.extract_features(image_folder_path=image_folder_path)
    lbp.save_features(f"{DATA_DIR}/lbp/run_{i}")
