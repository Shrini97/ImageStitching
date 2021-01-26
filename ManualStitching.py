from GetPoints import *
from HomographyMatrix import *

import numpy as np
import cv2

img_src1 = ""
img_src2 = ""

img1 = cv2.imread(img_src1)
img2 = cv2.imread(img_src2)

A, B = select_keypts(img1, img2)
H = homographic_matrix(A,B)
warped_image = cv2.warpPerspective(img2, H, img1.shape[0:2])
cv2.imshow("wide angle image", img1)
cv2.imshow("warped image space", warped_image)
cv2.waitKey(0)