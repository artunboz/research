import json
import os.path
import pickle
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from src.util.helpers import create_json_dict


class AbstractFeature(ABC):
    def __init__(self, resize_size: tuple[int, int]) -> None:
        """Inits an AbstractFeature instance. Should not be used outside subclasses.

        :param resize_size: A 2-tuple of integers indicating the pixel width and height
            of the resized image.
        """
        self.resize_size: tuple[int, int] = resize_size
        self.image_names: Optional[list[str]] = None
        self.image_features: Optional[np.ndarray] = None
        self.feature_dim: Optional[int] = None

    @abstractmethod
    def extract_features(self, image_folder_path: str) -> np.ndarray:
        """Extracts features from all the images found in the folder located at the
        given path and returns them in a 2-d numpy array of shape
        (n_images, n_features).

        :param image_folder_path: A string indicating the path to the folder containing
            the images.
        :return: A 2-d numpy array of shape (n_images, n_features).
        """

    @abstractmethod
    def read_image(self, image_path: str) -> np.ndarray:
        """Reads the image found in the given path and returns the image as a numpy
        array.

        :param image_path: A string indicating the path to the image.
        :return: A numpy array containing the image.
        """

    def get_config(self) -> dict:
        """Returns the configuration of the feature as a dictionary.

        :return: A dictionary containing the configuration of the feature.
        """
        if self.image_features is not None:
            self.feature_dim = self.image_features.shape[1]

        config: dict = create_json_dict(vars(self))
        del config["image_names"]
        config["resize_size"] = "x".join(map(str, config["resize_size"]))
        return config

    def save_features(self, save_folder_path: str) -> None:
        """Saves the computed features as a pickled ndarray, the names of the images as
        a pickled list, and the configuration as a JSON file to the folder with the
        given path.

        :param save_folder_path: A sting indicating the folder to save the files to.
        """
        if self.image_names is None or self.image_features is None:
            raise ValueError("The features have not been computed yet.")

        if not os.path.isdir(save_folder_path):
            os.mkdir(save_folder_path)

        with open(f"{save_folder_path}/feature_config.json", mode="w") as f:
            json.dump(self.get_config(), f)
        with open(f"{save_folder_path}/image_names.pickle", mode="wb") as f:
            pickle.dump(self.image_names, f)
        np.save(f"{save_folder_path}/features.npy", self.image_features)
