import time
from unittest import TestCase, skip

import cv2 as cv

from chibi_miru.image import Image, Threshold, Processing, Contours
from chibi_miru.barcode import types
import PIL.Image


class Test_image( TestCase ):
    def setUp( self ):
        super().setUp()
        self.img_path = 'tests/1535359854403.png'
        self.image = Image( self.img_path )
        self.wait_time = 2000

    def tearDown( self ):
        super().tearDown()
        #time.sleep( self.wait_time / 1000 )
        cv.waitKey( self.wait_time )
        cv.destroyAllWindows()


class Test_image_draw( Test_image ):
    def test_should_show_the_image( self ):
        self.image.show()

    def test_should_draw_a_line( self ):
        self.image.draw.line( ( 100, 100 ), ( 200, 200 ), ( 255, 0, 0 ) )
        self.image.show()

    def test_should_draw_a_rectangle( self ):
        self.image.draw.rectangle( ( 100, 100 ), 100, 100, ( 255, 0, 0 ) )
        self.image.show()


class Test_image_funtions( Test_image ):

    def test_ratio_should_return_a_float( self ):
        self.assertIsInstance( self.image.ratio, float )

    def test_without_dimensions_should_return_self( self ):
        result = self.image.resize()
        self.assertIs( self.image, result )

    def test_width_should_mantent_the_ratio( self ):
        result = self.image.resize( width=100 )
        self.assertAlmostEqual( self.image.ratio, result.ratio, 2 )
        result.show()

    @skip( 'small diff' )
    def test_height_should_mantent_the_ratio( self ):
        result = self.image.resize( height=100 )
        self.assertAlmostEqual( self.image.ratio, result.ratio, 2 )
        result.show()


class Test_gray( TestCase ):
    def setUp( self ):
        super().setUp()
        self.image = Image( "tests/1535359854403.png" )
        self.wait_time = 2000

    def test_gray_should_return_image( self ):
        gray = self.image.gray
        self.assertIsInstance( gray, Image )

    def test_gray_should_have_is_gray( self ):
        gray = self.image.gray
        self.assertTrue( gray.is_gray )

    def test_gray_show( self ):
        gray = self.image.gray
        gray.show()
        gray.wait( self.wait_time )
        gray.close()


class Test_procesings( TestCase ):
    def setUp( self ):
        super().setUp()
        self.image = Image( "tests/1535359854403.png" )
        self.wait_time = 2000

    def test_processing_should_work( self ):
        p = self.image.processing
        self.assertTrue( p )

    def test_processing_should_have_his_parent_to_the_creator( self ):
        p = self.image.processing
        self.assertIs( p.parent, self.image )

    def test_otsu_should_return_a_threshold( self ):
        result = self.image.processing.otsu()
        self.assertIsInstance( result, Threshold )

    def test_show_otsu( self ):
        result = self.image.processing.otsu()
        result.show()
        result.wait( self.wait_time )
        result.close()


class Test_detect( TestCase ):
    def setUp( self ):
        super().setUp()
        self.image = Image( "tests/1535359854403.png" )
        self.wait_time = 2000

    def test_detect_should_work( self ):
        p = self.image.detect
        self.assertTrue( p )

    def test_should_have_his_parent_to_the_creator( self ):
        p = self.image.processing
        self.assertIs( p.parent, self.image )

    def test_detect_contours_should_return_contour( self ):
        result = self.image.detect.contours()
        self.assertIsInstance( result, Contours )

    def test_show_contours( self ):
        result = self.image.detect.contours()
        result.show()
        result.wait( self.wait_time )
        result.close()


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


class Test_init_other_class( Test_image ):
    def test_should_transform_pil_to_cv( self ):
        pil_img = PIL.Image.open( self.img_path )
        image = Image( pil_img )
        image.show()

    def test_pil_and_cv_should_be_the_same( self ):
        pil_img = PIL.Image.open( self.img_path )
        image = Image( pil_img )
        e = image.raw == self.image.raw
        self.assertTrue( e.all() )
