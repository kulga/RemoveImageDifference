#!/usr/bin/env python3

import sys
import argparse

import numpy as np
from PIL import Image

class ImageArray():
    '''
    Load each image into a array, stack on top on other image arrays
    and run _process_image
    '''
    def __init__(self, images):
        self.images = (self._load_image(image)
                       for image in images)
        self.stacked_image_arrays = np.stack(self.images)
        self.flattened_image_array = self._process_image(self.stacked_image_arrays)

    def _load_image(self, _file):
        with Image.open(_file) as img:
            return np.array(img)

    def save_image(self, save_location):
        image = Image.fromarray(self.flattened_image_array.astype('uint8'))
        image.save(save_location)
        print(f'Saved to {save_location}')

    def _process_image(self):
        pass


class ImageMedian(ImageArray):
    '''Collapse image array into median of each pixel'''
    def __init__(self, images):
        super().__init__(images)

    def _process_image(self, stacked_image_arrays):
        if len(stacked_image_arrays) < 3:
            raise ValueError('Requires 3 or more images')
        flattened_median_image_array = np.median(stacked_image_arrays, axis=0)
        return flattened_median_image_array


class ImageMean(ImageArray):
    '''Collapse image array into mean of each pixel'''
    def __init__(self, images):
        super().__init__(images)

    def _process_image(self, stacked_image_arrays):
        flattened_mean_image_array = np.mean(stacked_image_arrays, axis=0)
        return flattened_mean_image_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Merge Common Pictures')
    parser.add_argument('-o', '--output',
            default='output.jpg')
    args, source_images = parser.parse_known_args()

    DemoImages = ImageMedian(source_images)
    #DemoImages = ImageMean(source_images)
    DemoImages.save_image(args.output)
