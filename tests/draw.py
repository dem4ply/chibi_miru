import time
from unittest import TestCase
from chibi_miru.draw import to_bgr

import cv2 as cv

from chibi_miru.image import Image


class Test_draw( TestCase ):
    def test_transform_rgb_to_bgr_tuple( self ):
        self.assertEqual( ( 255, 0, 0 ), to_bgr( ( 0, 0, 255 ) ) )
        self.assertEqual( ( 0, 255, 0 ), to_bgr( ( 0, 255, 0 ) ) )
        self.assertEqual( ( 0, 0, 255 ), to_bgr( ( 255, 0, 0 ) ) )

    def test_transform_rgb_to_bgr_list( self ):
        self.assertEqual( [ 255, 0, 0 ], to_bgr( [ 0, 0, 255 ] ) )
        self.assertEqual( [ 0, 255, 0 ], to_bgr( [ 0, 255, 0 ] ) )
        self.assertEqual( [ 0, 0, 255 ], to_bgr( [ 255, 0, 0 ] ) )
