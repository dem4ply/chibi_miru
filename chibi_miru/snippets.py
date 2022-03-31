import numpy as np


def pil_to_cv( pil_img ):
    pil_image = pil_img.convert( 'RGB' )
    open_cv_image = np.array( pil_image )
    # Convert RGB to BGR
    return open_cv_image[ :, :, ::-1 ].copy()
