import cv2 as cv
from skimage.metrics import structural_similarity
from skimage.transform import resize
import numpy as np
import math 
from cgi import test

file = r"C:\Users\John\Downloads\Reference_Image\reference_single_fire.png"
file = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\ScreenShot00000.png"
image = cv.imread(file)

x, y, w, h = 519, 11, 557, 1019
image = image[y:y+h, x:x+w]

cv.imwrite(r"C:\Users\John\Downloads\Reference_Image\unreal_cropped.png", image)

# cv.imshow("image", image)

# cv.waitKey(0)

# cv.destroyAllWindows()