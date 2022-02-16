import time
from unittest import TestCase

import cv2 as cv

from chibi.miru.image import Image
from chibi.miru.barcode import types


class Test_image( TestCase ):
    def setUp( self ):
        super().setUp()
        self.image = Image( "tests/1535359854403.png" )
        self.wait_time = 2000

    def tearDown( self ):
        super().tearDown()
        cv.waitKey( self.wait_time )
        cv.destroyAllWindows();


class Test_image_draw( Test_image ):
    def test_should_show_the_image( self ):
        self.image.show()

    def test_should_draw_a_line( self ):
        self.image.draw.line( ( 100, 100 ), ( 200, 200 ), ( 255, 0, 0 ) )
        self.image.show()

    def test_should_draw_a_rectangle( self ):
        self.image.draw.rectangle( ( 100, 100 ), 100, 100, ( 255, 0, 0 ) )
        self.image.show()


class Test_image_qr( Test_image ):
    def setUp( self ):
        super().setUp()
        self.image = Image( "tests/qr.png" )

    def test_detect_the_barcode( self ):
        qr = self.image.barcode.barcodes[0]
        self.assertIsInstance( qr, types.QR )
        self.assertEqual(
            'WIFI:S:TP-LINK_6034;T:WPA;P:73683698;;',
            str( qr ) )

    def test_draw_a_rectangle_in_the_barcode( self ):
        qr = self.image.barcode.barcodes[0]
        self.image.draw.barcode_boundary( qr, ( 255, 0, 0 ), 3 )
        self.image.show()
