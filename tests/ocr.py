import cv2 as cv
import pytesseract

from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi_miru.image import Image


class Test_image( TestCase ):
    def setUp( self ):
        super().setUp()
        self.img_path = (
            'tests/danbooru_3680001_5987123c26d87001a53d37d997424373.png' )
        self.image = Image( self.img_path )
        self.wait_time = 2000
        self.text_boxs = [
            # parafos del lado izquierdo
            ( ( 115, 300 ), ( 1052, 630 ) ),
            ( ( 115, 660 ), ( 1170, 900 ) ),
            ( ( 115, 920 ), ( 1190, 1160 ) ),
            ( ( 115, 1450 ), ( 1120, 1800 ) ),
            ( ( 110, 2600), ( 1380, 2730 ) ),
        ]
        self.text_on_box = {
            self.text_boxs[0]: (
                'OSS operates domestically as well as abroad, in\n'
                'either case, "Envoys" play a critical role in shaping\n'
                "the public\'s perception of the organisation.\nOverseas, "
                "they are ambassadors of the Empire,\nwhile in Imperial "
                "principalities they represent the\n0SS and by "
                "extension, the Emperor\'s government.\n"
            ),
            self.text_boxs[1]: (
                'Envoys rarely take parts in Direct Actions and are more\n'
                'often seen in various ceremonies. Both their skillsets\n'
                'and their equipment are designed more for handling\n'
                'formal occasions than for intense combat.\n'
            ),
            self.text_boxs[2]: (
                'The actual scope of their duties, however, is very vaguely\n'
                'defined, sometimes one or two Envoys can be seen in a\n'
                "delegation full of diplomats, other times they're spotted\n"
                'working alongside military operatives in covert operations.\n'
            ),
            self.text_boxs[3]: (
                "0SS Agent's Gas Mask\n"
                '\n'
                'The mask prohibits proper ADS so aiming the rifle is\n'
                "achieved using the mask's AR visor. Once calibrated,\n"
                "the AR projection is fixed to the user's facial tattoo\n"
                'rather than the visor, so the system can maintain a\n'
                'decent accuracy even when the mask itself has shifted.\n'
            ),
            self.text_boxs[4]: (
                "The visor's opacity can be adjusted. "
                "Paintings on the mask are useful\n"
                "for indentification amongst teammates "
                "when the mask's fully opaque.\n"
            ),
        }

    def tearDown( self ):
        super().tearDown()
        # time.sleep( self.wait_time / 1000 )
        cv.waitKey( self.wait_time )
        cv.destroyAllWindows()


class Test_ocr( Test_image ):
    def setUp( self ):
        super().setUp()
        self.temp_path = Chibi_temp_path()

    def test_ocr_should_work( self ):
        contours = self.image.detect._ocr_contours()
        crops = list( contours.crops() )
        self.assertTrue( crops )
        for section in crops:
            result = pytesseract.image_to_string( section.raw )
            self.assertTrue( result )

    def test_show_image( self ):
        image = self.image.resize( width=None, height=600 )
        contours = image.detect._ocr_contours()
        crops = list( contours.crops() )
        image.show()
        self.assertTrue( crops )
        for section in crops:
            result = pytesseract.image_to_string( section.raw )
            self.assertTrue( result )

    def test_cut_texts( self ):
        self.image.save( self.temp_path )
        crops = {}
        for box in self.text_boxs:
            xy1, xy2 = box
            x1, y1 = xy1
            x2, y2 = xy2
            width = abs( x1 - x2 )
            height = abs( y1 - y2 )
            crop = self.image.crop( x1, y1, width, height )
            crops[ box ] = crop
            crop.save( self.temp_path )
            self.image.draw.rectangle( xy1, width, height, ( 255, 0, 0 ) )

        for k, crop in crops.items():
            text = crop.detect.ocr.to_string()
            if k not in self.text_on_box:
                print()
                print( self.temp_path )
                print()
                print( k )
                print( text )
                import pdb
                pdb.set_trace()
                pass
            else:
                self.assertEqual( text, self.text_on_box[k] )
        self.image.name = "with_cuts.png"
        self.image.save( self.temp_path )
