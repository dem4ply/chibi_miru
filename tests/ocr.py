import cv2 as cv
import PIL.Image
from io import BytesIO
import pytesseract

from unittest import TestCase, skip
from chibi_miru.image import Image, Threshold, Contours
from chibi_miru.barcode import types

from chibi.file.temp import Chibi_temp_path


class Test_image( TestCase ):
    def setUp( self ):
        super().setUp()
        self.img_path = 'tests/danbooru_3680001_5987123c26d87001a53d37d997424373.png'
        self.image = Image( self.img_path )
        self.wait_time = 2000

    def tearDown( self ):
        super().tearDown()
        #time.sleep( self.wait_time / 1000 )
        cv.waitKey( self.wait_time )
        cv.destroyAllWindows()


class Test_ocr( Test_image ):
    def test_ocr_should_work( self ):
        contours = self.image.detect._ocr_contours()
        for section in contours.crops():
            result = pytesseract.image_to_string( section.raw )
            self.assertTrue( result )
