import time
import numpy
from chibi_miru.cam import Chibi_cam
from chibi_miru.image import Image
from unittest import TestCase


class Test_chibi_cam( TestCase ):
    def setUp( self ):
        pass

    def test_init_should_start_a_cam( self ):
        cam = Chibi_cam()
        self.assertEqual( 0, cam.cam_number )
        self.assertTrue( cam.is_open )

    def test_when_is_destroy_should_release_the_cam( self ):
        cam = Chibi_cam()
        _cam = cam._cam
        del cam
        self.assertFalse( _cam.isOpened() )


class Test_chibi_cam_read_img( TestCase ):
    def setUp( self ):
        pass

    def test_read_should_return_a_image( self ):
        cam = Chibi_cam()
        f = cam.read
        self.assertIsInstance( f, Image )
        self.assertIsInstance( f.raw, numpy.ndarray )
        f.show()
        f.wait( 2000 )
        f.close()

    def test_raw_read_should_return_a_ndarray( self ):
        cam = Chibi_cam()
        f = cam.raw_read
        self.assertIsInstance( f, numpy.ndarray )
        self.assertNotIsInstance( f, Image )
