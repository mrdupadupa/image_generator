#!/usr/bin/env python
# coding: utf-8

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from skimage.draw import (polygon as draw_polygon)
from skimage.draw import ellipse
from skimage.draw import (ellipse as draw_ellipse)
from skimage._shared.utils import warn


def draw_disk(center, radius, *, shape=None):
    """Generate coordinates of pixels within circle.
    Parameters
    ----------
    center : tuple
        Center coordinate of disk.
    radius : double
        Radius of disk.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output
        pixel coordinates. This is useful for disks that exceed the image
        size. If None, the full extent of the disk is used.  Must be at least
        length 2. Only the first two values are used to determine the extent of
        the input image.
    Returns
    -------
    rr, cc : ndarray of int
        Pixel coordinates of disk.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.

    """
    r, c = center
    return ellipse(r, c, radius, radius, shape)

# Generate different masks

def _generate_rectangle_mask(point, image, shape, random):
    """Generate a mask for a filled rectangle shape.
    The height and width of the rectangle are generated randomly.
    Parameters
    ----------
    point : tuple
        The row and column of the top left corner of the rectangle.
    image : tuple
        The height, width and depth of the image into which the shape is placed.
    shape : tuple
        The minimum and maximum size of the shape to fit.
    random : np.random.RandomState
        The random state to use for random sampling.
    Raises
    ------
    ArithmeticError
        When a shape cannot be fit into the image with the given starting
        coordinates. This usually means the image dimensions are too small or
        shape dimensions too large.
    Returns
    -------
    label : tuple
        A (category, ((r0, r1), (c0, c1))) tuple specifying the category and
        bounding box coordinates of the shape.
    indices : 2-D array
        A mask of indices that the shape fills.
    """
    available_width = min(image[1] - point[1], shape[1])
    if available_width < shape[0]:
        raise ArithmeticError('cannot fit shape to image')
    available_height = min(image[0] - point[0], shape[1])
    if available_height < shape[0]:
        raise ArithmeticError('cannot fit shape to image')
    # Pick random widths and heights.
    r = random.randint(shape[0], available_height + 1)
    c = random.randint(shape[0], available_width + 1)
    rectangle = draw_polygon([
        point[0],
        point[0] + r,
        point[0] + r,
        point[0],
    ], [
        point[1],
        point[1],
        point[1] + c,
        point[1] + c,
    ])
    label = ('rectangle', ((point[0], point[0] + r), (point[1], point[1] + c)))

    return rectangle, label


def _generate_circle_mask(point, image, shape, random):
    """Generate a mask for a filled circle shape.
    The radius of the circle is generated randomly.
    Parameters
    ----------
    point : tuple
        The row and column of the top left corner of the rectangle.
    image : tuple
        The height, width and depth of the image into which the shape is placed.
    shape : tuple
        The minimum and maximum size and color of the shape to fit.
    random : np.random.RandomState
        The random state to use for random sampling.
    Raises
    ------
    ArithmeticError
        When a shape cannot be fit into the image with the given starting
        coordinates. This usually means the image dimensions are too small or
        shape dimensions too large.
    Returns
    -------
    label : tuple
        A (category, ((r0, r1), (c0, c1))) tuple specifying the category and
        bounding box coordinates of the shape.
    indices : 2-D array
        A mask of indices that the shape fills.
    """
    if shape[0] == 1 or shape[1] == 1:
        raise ValueError('size must be > 1 for circles')
    min_radius = shape[0] / 2.0
    max_radius = shape[1] / 2.0
    left = point[1]
    right = image[1] - point[1]
    top = point[0]
    bottom = image[0] - point[0]
    available_radius = min(left, right, top, bottom, max_radius)
    if available_radius < min_radius:
        raise ArithmeticError('cannot fit shape to image')
    radius = random.randint(min_radius, available_radius + 1)
    # TODO: think about how to deprecate this
    # while draw_circle was deprecated in favor of draw_disk
    # switching to a label of 'disk' here
    # would be a breaking change for downstream libraries
    # See discussion on naming convention here
    # https://github.com/scikit-image/scikit-image/pull/4428
    disk = draw_disk((point[0], point[1]), radius)
    # Until a deprecation path is decided, always return `'circle'`
    label = ('circle', ((point[0] - radius + 1, point[0] + radius),
                        (point[1] - radius + 1, point[1] + radius)))

    return disk, label


def _generate_triangle_mask(point, image, shape, random):
    """Generate a mask for a filled equilateral triangle shape.
    The length of the sides of the triangle is generated randomly.
    Parameters
    ----------
    point : tuple
        The row and column of the top left corner of a down-pointing triangle.
    image : tuple
        The height, width and depth of the image into which the shape is placed.
    shape : tuple
        The minimum and maximum size and color of the shape to fit.
    random : np.random.RandomState
        The random state to use for random sampling.
    Raises
    ------
    ArithmeticError
        When a shape cannot be fit into the image with the given starting
        coordinates. This usually means the image dimensions are too small or
        shape dimensions too large.
    Returns
    -------
    label : tuple
        A (category, ((r0, r1), (c0, c1))) tuple specifying the category and
        bounding box coordinates of the shape.
    indices : 2-D array
        A mask of indices that the shape fills.
    """
    if shape[0] == 1 or shape[1] == 1:
        raise ValueError('dimension must be > 1 for triangles')
    available_side = min(image[1] - point[1], point[0] + 1, shape[1])
    if available_side < shape[0]:
        raise ArithmeticError('cannot fit shape to image')
    side = random.randint(shape[0], available_side + 1)
    triangle_height = int(np.ceil(np.sqrt(3 / 4.0) * side))
    triangle = draw_polygon([
        point[0],
        point[0] - triangle_height,
        point[0],
    ], [
        point[1],
        point[1] + side // 2,
        point[1] + side,
    ])
    label = ('triangle', ((point[0] - triangle_height, point[0]),
                          (point[1], point[1] + side)))

    return triangle, label

# different scenarious description:

SHAPE_GENERATORS_ALL = dict(
    rectangle=_generate_rectangle_mask,
    triangle=_generate_triangle_mask,
    circle=_generate_circle_mask
    #ellipse=_generate_ellipse_mask
    )
SHAPE_GENERATORS_R_T = dict(
    rectangle=_generate_rectangle_mask,
    #circle=_generate_circle_mask,
    triangle=_generate_triangle_mask
    #ellipse=_generate_ellipse_mask
    )
SHAPE_GENERATORS_C = dict(
    #rectangle=_generate_rectangle_mask,
    circle=_generate_circle_mask
    #triangle=_generate_triangle_mask,
    #ellipse=_generate_ellipse_mask
    )

SHAPE_CHOICES_ALL = list(SHAPE_GENERATORS_ALL.values())
SHAPE_CHOICES_R_T = list(SHAPE_GENERATORS_R_T.values())
SHAPE_CHOICES_C = list(SHAPE_GENERATORS_C.values())


def _generate_random_colors(num_colors, num_channels, intensity_range, random):
       
    if num_channels == 1:
        intensity_range = (intensity_range, )
    elif len(intensity_range) == 1:
        intensity_range = intensity_range * num_channels
    colors = [random.randint(r[0], r[1]+1, size=num_colors)
              for r in intensity_range]
    return np.transpose(colors)


def random_shapes(image_shape,
                  max_shapes,
                  min_shapes=1,
                  min_size=2,
                  max_size=None,
                  multichannel=True,
                  num_channels=3,
                  shape=None,
                  scenario='SHAPEGENERATOR_ALL_HALO',
                  #my_shape_list=[1,2,3]
                  intensity_range=None,
                  allow_overlap=False,
                  num_trials=100,
                  random_seed=None):
        
    
    if min_size > image_shape[0] or min_size > image_shape[1]:
        raise ValueError('Minimum dimension must be less than ncols and nrows')
    max_size = max_size or max(image_shape[0], image_shape[1])

    if not multichannel:
        num_channels = 1

    if intensity_range is None:
        intensity_range = (0, 254) if num_channels == 1 else ((0, 254), )
    else:
        tmp = (intensity_range, ) if num_channels == 1 else intensity_range
        for intensity_pair in tmp:
            for intensity in intensity_pair:
                if not (0 <= intensity <= 255):
                    msg = 'Intensity range must lie within (0, 255) interval'
                    raise ValueError(msg)

    random = np.random.RandomState(random_seed)
    user_shape = shape
    #shape_list = 
    image_shape = (image_shape[0], image_shape[1], num_channels)
    image = np.full(image_shape, 255, dtype=np.uint8)
    filled = np.zeros(image_shape, dtype=bool)
    labels = []

    num_shapes = random.randint(min_shapes, max_shapes + 1)
    
    colors = _generate_random_colors(num_shapes, num_channels,
                                     intensity_range, random)
    for shape_idx in range(num_shapes):
        if user_shape is None:
    
    #run differen scenarious, two of them with probability as well
            if scenario == 'SHAPEGENERATOR_ALL_HALO':
                shape_generator = random.choice(SHAPE_CHOICES_ALL, p=[0.45, 0.45, 0.1])
    
            elif scenario == 'SHAPEGENERATOR_ALL_CORE':
                shape_generator = random.choice(SHAPE_CHOICES_ALL, p=[0.1, 0.1, 0.8])
    #rectangles and triangles
            elif scenario == 'SHAPEGENERATOR_R_T':
                shape_generator = random.choice(SHAPE_CHOICES_R_T)
    #only circles
            elif scenario == 'SHAPEGENERATOR_C':
                shape_generator = random.choice(SHAPE_CHOICES_C)
    
            else:
                print("Error in the script")
            
        else:
            shape_generator = SHAPE_GENERATORS_ALL[user_shape]
        shape = (min_size, max_size)
        for _ in range(num_trials):
            # Pick start coordinates.
            column = random.randint(image_shape[1])
            row = random.randint(image_shape[0])
            point = (row, column)
            try:
                indices, label = shape_generator(point, image_shape, shape,
                                                 random)
            except ArithmeticError:
                # Couldn't fit the shape, skip it.
                continue
            # Check if there is an overlap where the mask is nonzero.
            if allow_overlap or not filled[indices].any():
                image[indices] = colors[shape_idx]
                filled[indices] = True
                labels.append(label)
                break
        else:
            warn('Could not fit any shapes to image, '
                 'consider reducing the minimum dimension')

    if not multichannel:
        image = np.squeeze(image, axis=2)
    return image, labels
