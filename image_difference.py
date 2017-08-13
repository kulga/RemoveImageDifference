#!/usr/bin/env python3

import sys
import argparse

from collections import Counter
from statistics import median

import numpy as np
from PIL import Image

import line_profiler

class ImageDifference():
    def __init__(self, images):
        self.images = (self.load_image(image)
                       for image in images)
        self.source_image_array = self.load_image(images[0])

        self.images_array = (self.location_array(image)
                             for image in self.images)

        for row_index, column_index, bit_array in self.create_bit_list(self.images_array):
            self.source_image_array[row_index][column_index] = bit_array

    def location_array(self, array):
        '''Get location and array for each pixel'''
        return ((row_index, column_index, pixel_array)
                for row_index, row in enumerate(array)
                for column_index, pixel_array in enumerate(row)
               )

    def create_bit_list(self, image_arrays):
        '''
        Find most common pixel for each pixel in image_arrays
        All images must have identical dimensions
        '''
        for zipped_location_pixel in zip(*zipped_location_pixels):
            row_index = zipped_location_pixel[0][0]
            column_index = zipped_location_pixel[0][1]
            pixel_list = (tuple(location_pixel[2]) for location_pixel in zipped_location_pixel)
            median_pixel_list = tuple(median(pixel_zipped_array) 
                                 for pixel_zipped_array in zip(*pixel_list))
            common_pixel = np.array([int(num) for num in median_pixel_list], dtype='uint8')
            
            yield (row_index, column_index, common_pixel)

    def load_image(self, _file):
        with Image.open(_file) as img:
            img.convert('L')
            return np.array(img)

    def save_image(self, save_location):
        image = Image.fromarray(self.source_image_array)
        image.save(save_location)
        print('Saved to {}'.format(save_location))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Merge Common Pictures')
    parser.add_argument('-o', '--output')
    args, other_args = parser.parse_known_args()

    DemoImages = ImageDifference(other_args)
    DemoImages.save_image(args.output)

