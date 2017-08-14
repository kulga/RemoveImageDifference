#!/usr/bin/env python3

import sys
import argparse

import numpy as np
from PIL import Image

class RemoveImageDifference():
    def __init__(self, images):
        self.images = (self._load_image(image)
                       for image in images)
        self.stacked_image_arrays = np.stack(self.images, axis=3)
        self.flattened_image = np.mean(self.stacked_image_arrays, axis=3)

    def _load_image(self, _file):
        with Image.open(_file) as img:
            return np.array(img)

    def save_image(self, save_location):
        image = Image.fromarray(self.flattened_image.astype('uint8'))
        image.save(save_location)
        print('Saved to {}'.format(save_location))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Merge Common Pictures')
    parser.add_argument('-o', '--output')
    args, source_images = parser.parse_known_args()

    DemoImages = RemoveImageDifference(source_images)
    DemoImages.save_image(args.output)
