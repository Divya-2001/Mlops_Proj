def filter(destination):
    import cv2
    import numpy as np
    import scipy
    img = cv2.imread(destination)
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("greyscale",greyscale)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return greyscale
