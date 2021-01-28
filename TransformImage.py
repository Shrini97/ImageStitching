from GetPoints import *
from HomographyMatrix import *

import numpy as np
import cv2

def transform(list_bbox, zoom_image, wide_image, H):
    '''
    Returns the transformed image and bbox coordinates given 
    a homography matrix H
    Args:
        list_bbox (List): a list of numpy array [ [[x1,y1],[x2,y2]].... ]
        image (np.ndarray): a 3 channel ncv2 image
        H (np.ndarray): the homography matrix required for the warp
    Returns:
        A list of warped bbox coordinates and the transformed image
    '''
    h, w, _ = wide_image.shape
    zoom_image_transformed = cv2.warpPerspective(wide_image, H, (w,h))
    transformed_bbox = []
    for elem in list_bbox:
        elem_homogeneous = np.ones((3,2))
        elem_homogeneous[0:2, 0:2] = elem.T
        elem_transformed = np.matmul(H, elem_homogeneous)
        elem_transformed[:,0] = elem_transformed[:, 0]/elem_transformed[2, 0]
        elem_transformed[:,1] = elem_transformed[:, 1]/elem_transformed[2, 1]
        elem_transformed = elem_transformed.T[:,0:2]
        transformed_bbox.append(elem_transformed)
    return list_bbox, zoom_image_transformed 
         
